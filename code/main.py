import networkx as nx
from pyvis.network import Network
import argparse
from pathlib import Path
import os

# Reading an instance file from the DIMACS library
def read_instance(file): 
    with open(file) as f:       # Open the file 
        edges = []              # Create a list of edges
        num_vertices = 0        # Create a int for the number of vertices/nodes
        for line in f:          # Read every line in the file
            if line[0] == "p":  # Lines that start with p are split and the number of vertices is filtered out
                as_list = line.split(" ")
                num_vertices = int(as_list[2])
            if line[0] == "e":  # Lines that start with e contain the edge information, these are safed as tuple in a list
                as_list = line.rstrip("\n").split(" ")
                edges.append((int(as_list[1]), int(as_list[2])))
    
    return edges, num_vertices  # Return the list of edges and number of vertices

def create_graph_from_edges(edges): # Simple function to create a Graph from a list of edges
    G = nx.DiGraph()                # Create a empty grpah instance
    G.add_edges_from(edges)         # Adds all edges from a list of tuples
    return G
        
def plot_graph(graph, visualize=False):     # Function gets a Graph and a boolean if the graph should be visualized
    net = Network(directed=True)            # Create an empty Network with directed arcs
    net.from_nx(graph)                      # Use the graph to fill the Network
    if visualize:                           # If the network should be visualized, it is saved in the html file, do NOT try to visualize complete instance from the benchmarks (long waiting time and not much to see)
        net.show('mygraph.html', notebook=False)
    return net

def transform_digraph_to_NFI():
    pass

def main():
    edges, num_vertices = read_instance("instances\\C125.9.clq")     #reading a instance ("folder\\file") 
    G = create_graph_from_edges(edges[0:10])        # creating a graph
    # for visualization or if you want to run the code on smaller instances edges[0:X], where X is the number of edges you want to use
    net = plot_graph(G, True)   # save the Network, if you say False here it will not be saved as html, but can be done so later on with net.show('mygraph.html', notebook=False)

if __name__ == "__main__":
    main()