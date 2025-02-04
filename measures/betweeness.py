import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint as pp
from util import df_to_graph


data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")

G = df_to_graph(data, weights="count", label="release_year")

# Compute Betweenness Centrality (weighted)
betweenness = nx.betweenness_centrality(G, weight="weight")
print(f"Betweenness Centrality:")
pp(betweenness)



# Draw graph with Betweenness Centrality
fig = plt.figure(figsize=(12, 12))
fig.canvas.manager.set_window_title("Betweenness Centrality")
pos = nx.spring_layout(G, seed=42)
node_sizes = [5000 * betweenness[n] for n in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color="lightcoral", edge_color="black", node_size=node_sizes, alpha=0.7)
fig.suptitle("Simplified Graph: Betweenness Centrality")

plt.show()
