import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edge(1, 2)
G.add_edge(2, 1)
G.add_edge(2, 3)
G.add_edge(3, 1)

print(list(nx.bfs_edges(G, 1)))

# nx.draw(G, with_labels=True)
# plt.show()