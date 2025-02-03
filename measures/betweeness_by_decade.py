import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint as pp
from util import decade_graphs


data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")
graphs_by_decade = decade_graphs(data, timestamp_label="release_year", weight_label="count")

b_centralities = []
for decade, graph in graphs_by_decade.items():
    # Compute Betweenness Centrality (weighted)
    betweenness = nx.betweenness_centrality(graph, weight="weight")
    print(f"Betweenness Centrality:")
    pp(betweenness)
    b_centralities.append(betweenness)
    


    # Draw graph with Betweenness Centrality
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph, seed=42)
    node_sizes = [5000 * betweenness[n] for n in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_color="lightcoral", edge_color="black", node_size=node_sizes, alpha=0.7)
    plt.title(f"{decade}: Betweenness Centrality")

    plt.show()

bc_df = pd.DataFrame(b_centralities, index=graphs_by_decade.keys())
print(bc_df)