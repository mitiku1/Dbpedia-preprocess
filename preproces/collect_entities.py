import os
import numpy as np
import pandas as pd
import hdt
import time
import glob;
import tqdm
def main():   
    for hdt_file in tqdm.tqdm(glob.glob("dbpedia-hdt/*.hdt")):
        _, filename = os.path.split(hdt_file)
        document = hdt.HDTDocument(hdt_file);
        triples, cardinality = document.search_triples("", "", "")
        entities = set()

        for triple in triples:
            entities.update(list(triple))


        with open(os.path.join("entities", filename[:-4]+".entities"), "w+") as output_file:
            for entity in entities:
                output_file.write(entity)
                output_file.write("\n")
    


if __name__=='__main__':
    main()