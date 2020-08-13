import os
import numpy as np
import pandas as pd
from graph_walk import WalkGenerator, TripleIteratorStore
from utils import get_configs
import argparse


def main(args):
    config = get_configs(args.config)
    triple_iter_store = TripleIteratorStore(config)
    walker = WalkGenerator(config, triple_iter_store, args.output_path)
    
    walker.generate_walks(args.num_walks)

    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Path to cofig file", default="config.yaml")
    parser.add_argument("-o", "--output_path", help="Directory to save random walks", default="logs/walks")
    parser.add_argument("-n", "--num_walks", help="Number of walks to generate", default=1000000, type=int)
    
    args = parser.parse_args()


    main(args)