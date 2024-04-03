import networkx as nx
from pyvis.network import Network
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import os

import gurobipy as gp
from gurobipy import GRB

import scipy.special as sci

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
    #G = nx.DiGraph()                # Create a empty grpah instance
    G = nx.MultiDiGraph()
    G.add_edges_from(edges)         # Adds all edges from a list of tuples
    
    return G

def compute_min_cut(graph):
    cut_value, partition = nx.minimum_cut(graph, 's', 't')
    # Return the nodes in the source and sink sets
    source_set, sink_set = partition
    return source_set, sink_set

        
def plot_graph(graph, visualize=False):     # Function gets a Graph and a boolean if the graph should be visualized
    net = Network(directed=True)            # Create an empty Network with directed arcs
    net.from_nx(graph)                      # Use the graph to fill the Network
    if visualize:                           # If the network should be visualized, it is saved in the html file, do NOT try to visualize complete instance from the benchmarks (long waiting time and not much to see)
        net.show('mygraph.html', notebook=False)
    return net

def mipmodel(first_layer_edges, second_layer_edges, third_layer_edges, node_list, K, B):  # edge_list is a list of tuples with indices for all edges 
                                            # node_list is a list of indices for all nodes
    m = gp.Model("mip1")

    # Create variables
    alpha = m.addVars(node_list, vtype=GRB.BINARY, name="alpha")
    edge_list = first_layer_edges + second_layer_edges + third_layer_edges # multiply by length of first_layer_edges = m = # of edges
    beta = m.addVars(edge_list, vtype=GRB.BINARY, name="beta")
    gamma = m.addVars(edge_list, vtype=GRB.BINARY, name="gamma")
    z = m.addVar(vtype=GRB.INTEGER, name="z")

    #m.setObjective(beta.sum('*', '*') + beta.sum('s', '*'), GRB.MINIMIZE)
    m.setObjective(z, GRB.MINIMIZE)
    #m.setObjective(2*beta.sum('s', '*'), GRB.MINIMIZE)

    m.addConstr(beta.sum('*', '*') + beta.sum('s', '*') == z)
    m.addConstr(z >= K)

    m.addConstrs(alpha[x] - alpha[y] + beta[x,y] + gamma[x,y] >= 0 for (x,y) in edge_list)

    m.addConstr(alpha["t"] - alpha["s"] == 1)

    m.addConstr(gamma.sum('*', '*') == B) # <= or ==

    m.addConstrs(beta[x,y] == 0 for (x,y) in first_layer_edges)
    m.addConstrs(gamma[x,y] == 0 for (x,y) in second_layer_edges+third_layer_edges)

    m.addConstrs(gamma[y, x] <= alpha[x] for (y,x) in edge_list)

    m.addConstr(beta.sum('*','*') == K)

    # # Add constraint: x + 2 y + 3 z <= 4
    # m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

    # # Add constraint: x + y >= 1
    # m.addConstr(x + y >= 1, "c1")

    return m

def mipmodel_new(second_layer_edges, vertice_nodes, edge_nodes, B):
    m = gp.Model("mip2")

    K = 2
    #K_assumed = 35
    # alpha is 1 if edge_node i is interdicted / not interdicted?
    # gamma is 1 if vertice_node j is in the clique /interdicted?
    alpha = m.addVars(edge_nodes, vtype=GRB.BINARY, name="alpha")
    gamma = m.addVars(vertice_nodes, vtype=GRB.BINARY, name="gamma")

    #m.setObjective(gamma.sum('*'), GRB.MINIMIZE)
    #m.setObjective(alpha.sum('*'), GRB.MAXIMIZE)
    m.setObjective(alpha.sum('*'), GRB.MINIMIZE)

    for (i,j) in second_layer_edges:
        #m.addConstr(gamma[j] >= (1-alpha[i]))
        #m.addConstr(alpha[i] <= (1-gamma[j]))
        m.addConstr(alpha[i] >= gamma[j])
    
    #m.addConstr(alpha.sum('*') >= 10000)
    m.addConstr(gamma.sum('*') == len(vertice_nodes) - K)

    # Testing a constraint that raises the objective value to the # of cliques
    #m.addConstr(alpha.sum('*') >= len (edge_nodes) - sci.binom(K, 2))

    return m


def main():
    edges, num_vertices = read_instance("instances/DSJC500_5.clq")     #reading a instance ("folder\\file") 
    #edges, num_vertices = read_instance("instances/test.clq")
    
    #num_vertices = 4
    #edges = [(1,2), (1,3), (2,3), (3,4), (2,4)]
    # Vertices = nodes in original graph, Nodes = nodes in NFI graph

    #edges = edges[0:300]

    node_list_edges = [f"i_{x}" for x in range(1,len(edges)+1)]
    node_list_vertices = [f"j_{x}" for x in range(1,num_vertices+1)]
    node_list = ["s"] + node_list_edges + node_list_vertices + ["t"]
  
    first_layer_edges = [("s",x) for x in node_list_edges]
    third_layer_edges = [(x,"t") for x in node_list_vertices]

    second_layer_edges = []
    iter = 1
    for (x,y) in edges:
        second_layer_edges.append((f"i_{iter}",f"j_{x}"))
        second_layer_edges.append((f"i_{iter}",f"j_{y}"))
        iter += 1

        


    # G = create_graph_from_edges(edges[0:10])        # creating a graph
    # # for visualization or if you want to run the code on smaller instances edges[0:X], where X is the number of edges you want to use
    # #net = plot_graph(G, True)   # save the Network, if you say False here it will not be saved as html, but can be done so later on with net.show('mygraph.html', notebook=False)

    # #first_layer_edges = [("s", x, {"capacity": 2*num_vertices}) for x in range(1,num_vertices+1)]
    # #first_layer_edges = [("s", f"x_{x}", {"capacity": 12}) for x in range(1,7)]
    # #third_layer_edges = [(f"y_{x}", "t", {"capacity": })]

    # edge_list = [(1,2), (1,3), (2,3), (2,4), (3,4)]
    # num_edges = len(edge_list)

    # edge_nodes = [f"i_{x}" for x in range(1,num_edges+1)]
    # first_layer_edges = [("s", x) for x in edge_nodes]
    # #print(first_layer_edges)
    # vertice_nodes = [f"j_{x}" for x in range(1,5)]
    # thrid_layer_edges = [(x, "t") for x in vertice_nodes]

    # second_layer = []
    # i = 1
    # for (x,y) in edge_list:
    #     second_layer.append((i, x))
    #     second_layer.append((i, y))
    #     i += 1

    # #print(second_layer)
    # second_layer_edges = [(f"i_{x}", f"j_{y}") for (x,y) in second_layer]

    # #print(second_layer_edges_one)

    # G2 = nx.DiGraph()
    # # G2.add_node("s", subset = "S")
    # # G2.add_nodes_from(edge_nodes, subset = "edges")
    # # G2.add_nodes_from(vertice_nodes, subset = "vertices")
    # # G2.add_node("t", subset = "T")
    # G2.add_edges_from(first_layer_edges, capacity = 2.4)
    # G2.add_edges_from(thrid_layer_edges, capacity = num_edges)
    # G2.add_edges_from(second_layer_edges, capacity = num_edges)

    # # pos = nx.multipartite_layout(G2)
    # # nx.draw(G2, pos=pos)
    # # plt.show()

    try: 

        K = 11
        B = len(edges) - sci.binom(K, 2)

        #m = mipmodel(first_layer_edges, second_layer_edges, third_layer_edges, node_list, K, B)
        m = mipmodel_new(second_layer_edges, node_list_vertices, node_list_edges, B)
        m.optimize()

        #print(m.getVars())

        #print(f"Here {m.alpha.VarName}")

        for v in m.getVars():
            if v.X != 0:
                print(f"{v.VarName} {v.X:g}")

        print(f"Obj: {m.ObjVal:g}")

    except gp.GurobiError as e:
        print(f"Error code {e.errno}: {e}")

    except AttributeError:
        print("Encountered an attribute error")



if __name__ == "__main__":
    main()