import networkx as nx
import matplotlib.pyplot as plt
from scip_shortest_path import make_random_instance

coords, distances = make_random_instance(100, 6, 10)

G = nx.Graph()

for i in range(len(coords)):
    G.add_node(i, pos=(coords[i, 0], coords[i, 1]), color='black')
for i, j in distances:
    G.add_edge(i, j, weight=distances[i, j], color='black')

# Find the shortest path from node 0 to node 99
path = nx.shortest_path(G, source=0, target=99, weight='weight', method='dijkstra')
print("Shortest path:", path)

# Get node positions
pos = nx.get_node_attributes(G, 'pos')

# Draw the full graph with default colors
nx.draw(G, pos=pos, with_labels=True, node_color='black', edge_color='gray')

# Create a list of edges from the path for highlighting
path_edges = list(zip(path, path[1:]))

# Highlight nodes and edges of the shortest path in red
nx.draw_networkx_nodes(G, pos=pos, nodelist=path, node_color='red')
nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, edge_color='red', width=2)

plt.show()