import networkx as nx
import matplotlib.pyplot as plt

data = (('a', 'b', 50), ('b', 'c', 60), ('b', 'e', 25),
        ('e', 'f', 20), ('z', 'n', 10), ('x', 'm', 25),
        ('v', 'p', 15))

G = nx.DiGraph()
for node1, node2, weight1 in data:
    G.add_edge(node1, node2, weight=-1)

min_lenght = 2
F = nx.DiGraph()  # filtered graphs

# check all edges with bellman_ford
for u, v in G.edges():
    vals, distances = nx.bellman_ford(G, u)
    if min(distances.values()) < - min_lenght:
        for u, v in vals.items():
            if v:
                F.add_edge(v, u)

nx.draw(F)
plt.show()
