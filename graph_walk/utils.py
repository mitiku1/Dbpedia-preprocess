import numpy as np
import os
import hdt
import time

def get_triple_iterator(file_path):
    document = hdt.HDTDocument(file_path);
    triple_iterator, cardinality = document.search_triples("", "", "")
    return {"triple_iter":triple_iterator, "handler":document}

def get_triple_iterators_from_config(config):
    
    iterators = {}
    for relation in config["relations"]:
        hdt_file = os.path.join(config["data"]["path"], relation+".hdt")

        triple_iterator = get_triple_iterator(hdt_file)

        iterators[hdt_file] = triple_iterator
    return iterators


class TripleIteratorStore:
    def __init__(self, config):
        super().__init__()
        self.iterators = get_triple_iterators_from_config(config)
        self.config = config
        self.keys = list(self.iterators.keys())
        self.key2index = {self.keys[i]:i for i in range(len(self.keys))}
        self.index2key = {value:key for key, value in self.key2index.items()}
    def get_random_iter(self):
        return np.random.choice(self.keys)
    def get_next_triplet(self, key):
        try:
            return next(self.iterators[key]["triple_iter"])
        except StopIteration:
            self.iterators[key] = get_triple_iterator(key)
            return next(self.iterators[key]["triple_iter"])

    
    def get_iterator(self, key):
        return self.iterators[key]
    def get_out_going_edges(self, iterator, node):
        triples, _ = self.iterators[iterator]["handler"].search_triples(node, "", "")
        return list(triples)
    def sanitize_node_name(self, name):
        index = name.find("\"^^<")
        if index == -1:
            return name
        else:
            return name[index + 4:-1]

    def get_neighbors_all(self, node):
        output = []
        for key in self.keys:
            triples, _ = self.iterators[key]["handler"].search_triples(node, "", "")
            output.extend([self.sanitize_node_name(triple[2]) for triple in triples])
        return output


class WalkGenerator:
    
    def __init__(self, config, triple_iter_store, save_dir = None):
        """Walk generator class. The generations of the walk is parameterized by r and p.
        Note:

        Args:
            length (int): The maximum length of the walk to be generated.
            r (int): The parameter which controls probability to jumpy to other layers.
            triple_iter_store (TripleIteratorStore): TripleIteratorStore object containing triple iterator for each relation.

        """
        super().__init__()
        self.config = config
        self.triple_iter_store = triple_iter_store
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(self.save_dir)
    def __iter__(self):
        return self
    def generate_walks(self, num_walks = 1000):
        self.current_iter = self.triple_iter_store.get_random_iter()
        self.current_node = self.triple_iter_store.get_next_triplet(self.current_iter)[0]
        self.num_generated_walks = 0
        save_file_path = os.path.join(self.save_dir, "walks.{}".format(int(time.time())))
        iteration = 0
        while self.num_generated_walks < num_walks:
            walks, node = self.generate_rooted_walks(self.current_node)
            with open(save_file_path, "a+") as output_file:
                for walk in walks:
                    if len(walk) > self.config["graph-walk"]["min_length"]:
                        line = ",".join(list(map(str, map(hash, walk))))
                        output_file.write("{}\n".format(line))
            self.num_generated_walks += len(walks)
            if node is None:
                self.current_node = self.triple_iter_store.get_random_iter()
            else:
                self.current_iter = self.triple_iter_store.get_random_iter()
                self.current_node = self.triple_iter_store.get_next_triplet(self.current_iter)[0]
            if iteration % 100 == 0:
                print("Generated: {} walks".format(self.num_generated_walks))
            iteration+=1
                
    def generate_rooted_walks(self, root):
        walks = {(root, )}
        current_depth = 0
        last_neighbor = None
        while (current_depth < self.config["graph-walk"]["depth"]):
            walks_copy = set(walks)

            for walk in walks_copy:
                last_node = walk[-1]
                
                neighbors = self.triple_iter_store.get_neighbors_all(last_node)
                if len(neighbors) > 0:
                    walks.remove(walk)
                for neighbor in neighbors:
                    
                    walks.add(walk + (neighbor, ))
                    last_neighbor = neighbor
            walks = list(walks)

            choices = np.random.choice(len(walks), size=self.config["graph-walk"]["num_walks_per_node"])
            walks = {walks[index] for index in choices}
            current_depth+=1
        return walks, last_neighbor
        

