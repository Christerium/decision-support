import networkx as nx
from pyvis.network import Network

def compute_min_cut(graph):
    # Use networkx function to compute min cut
    cut_value, partition = nx.minimum_cut(graph, 's', 't')
    # Return the nodes in the source and sink sets
    source_set, sink_set = partition
    return source_set, sink_set

def visualize_graph(graph, source_set, sink_set):
    # Create a pyvis Network object
    net = Network()
    # Add nodes and edges to the pyvis network
    for node in graph.nodes():
        if node == 's':
            net.add_node(node, x=0)
        elif node == 'u' or node == 'w':
            net.add_node(node, x=100)
        elif node == 'v' or node == 'b':
            net.add_node(node, x=200)
        elif node == 't':
            net.add_node(node, x=300)
        else:
            net.add_node(node)
    for edge in graph.edges():
        if edge[0] in source_set and edge[1] in sink_set:
            net.add_edge(edge[0], edge[1], color="red", arrows="to")
        elif edge[0] in sink_set and edge[1] in source_set:
            net.add_edge(edge[0], edge[1], color="red", arrows="from")
        else:
            net.add_edge(edge[0], edge[1], color="gray", arrows="to")
    
    # Visualize the graph
    net.toggle_physics(True)
    net.show("graph_visualization.html", notebook=False)

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph
G.add_edge('s', 'u', capacity=7)
G.add_edge('s', 'w', capacity=4)
G.add_edge("s", "w", capacity=4)
G.add_edge('w', 'u', capacity=3)
G.add_edge('u', 'v', capacity=5)
G.add_edge('u', 'b', capacity=3)
G.add_edge('w', 'b', capacity=2)
G.add_edge('b', 'v', capacity=3)
G.add_edge('v', 't', capacity=8)
G.add_edge('b', 't', capacity=5)

# Compute min cut
source_set, sink_set = compute_min_cut(G)
print("Min Cut: ", source_set, sink_set)

# Visualize the graph
visualize_graph(G, source_set, sink_set)
