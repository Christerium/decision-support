import networkx as nx
from pyvis.network import Network
import argparse
from pathlib import Path

def read_instance(file):
    with open(file) as f:
        edges = []
        for line in f:
            if line[0] == e:
                as_list = line.split(" ")
                edges.append(as_list[1], as_list[2])


def main():
    inputfile = ''
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=Path)
    #parser.add_argument('-b', '--binary', type=int)
    args = parser.parse_args()
    inputfile = args.file

    read_instance(file)


if __name__ == "__main__":
    main()