import networkx as nx
from pyvis.network import Network
import argparse
from pathlib import Path
import os

def read_instance(file):
    with open(file) as f:
        edges = []
        num_vertices = 0
        for line in f:
            if line[0] == "p":
                as_list = line.split(" ")
                num_vertices = int(as_list[2])
            if line[0] == "e":
                as_list = line.rstrip("\n").split(" ")
                edges.append((int(as_list[1]), int(as_list[2])))
    
    return edges, num_vertices

def create_graph_from_edges(edges):
    G = nx.DiGraph()
    for e in edges:
        G.add_edge(*e)
    return G
        
def plot_graph(graph, visualize=False):
    net = Network(directed=True)
    net.from_nx(graph)
    net.repulsion()
    if visualize:
        net.show('mygraph.html', notebook=False)
    return net
        
def main():
    edges, num_vertices = read_instance("code\\C125.9.clq")
    G = create_graph_from_edges(edges[0:100])
    net = plot_graph(G, True)

if __name__ == "__main__":
    main()