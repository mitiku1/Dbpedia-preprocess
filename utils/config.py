import yaml
def get_current_relations(path = "current_relations.txt"):
    with open(path) as input_file:
        output = []
        for line in input_file.readlines():
            output.append(line.strip())
        return output

def get_configs(path = "./config.yaml"):
    with open(path) as f:
        output = yaml.load(f, yaml.FullLoader)
        output["relations"] = get_current_relations()
        return output
        