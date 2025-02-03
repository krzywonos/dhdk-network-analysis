import networkx as nx
import os
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint as pp
from statistics import median

data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")



data["decade"] = data["release_year"].apply(lambda x: str(x)[0:3] + "0s")
data_by_decade = data.groupby("decade", group_keys=False)

graphs_by_decade = {}
for decade, df in data_by_decade:
    graph = nx.Graph()
    for idx, row in df.iterrows():
        u = row.iloc[0]
        v = row.iloc[1]
        if graph.has_edge(u, v):
            graph[u][v]["weight"] += row["count"]
            graph[u][v]["year"].append(row["release_year"])
        else:
            graph.add_edge(u, v, year=[row["release_year"]], weight=row["count"])
    graphs_by_decade[decade] = graph

# Compute k-cores based on weights
def weighted_kcores(g:nx.Graph) -> dict:

    weighted_degrees = {node: sum(d["weight"] for _, _, d in g.edges(node, data=True)) for node in g.nodes()}
    print(weighted_degrees.values())
    k = round(median(sorted(weighted_degrees.values())))

    k_cores = {}
    graph = g.copy()    
    nodes_to_remove = [node for node, deg in weighted_degrees.items()
                        if deg < k]
    while nodes_to_remove:
        graph.remove_nodes_from(nodes_to_remove)
        weighted_degrees = {node: sum(d["weight"] for _, _, d in graph.edges(node, data=True)) for node in graph.nodes()}
        nodes_to_remove = [node for node, deg in weighted_degrees.items()
                            if deg < k]
    k_nodes = graph.nodes()
    if k_nodes:
        k_cores[(f"K value: {k}", f"Nodes: {len(k_nodes)}")] = list(k_nodes)
    return k_cores

decade_kcores = {decade: weighted_kcores(graph) for decade, graph in graphs_by_decade.items()}
pp(decade_kcores)
# # Graph representing our dataset
# GRAPH = nx.MultiGraph()

# for idx, row in data.iterrows():
#     u = row.iloc[0]
#     v = row.iloc[1]
#     GRAPH.add_edge(u, v, label=row["release_year"], weight=row["count"])

# # Simplified graph to perform measures, regardless of the year of publication
# G = nx.Graph()
# for u, v, data in GRAPH.edges(data=True):
#     if G.has_edge(u, v):
#         G[u][v]["weight"] += data["weight"]
#     else:
#         G.add_edge(u, v, weight=data["weight"])

# # Compute Betweenness Centrality (weighted)
# betweenness = nx.betweenness_centrality(G, weight="weight")
# print(f"Betweenness Centrality:")
# pp(betweenness)





# # Draw MultiGraph (GRAPH)
# plt.figure(figsize=(12, 12))
# pos = nx.spring_layout(GRAPH, seed=42)
# edge_weights = [d["weight"] for _, _, d in GRAPH.edges(data=True)]
# nx.draw(GRAPH, pos, with_labels=True, node_color="lightblue", edge_color="gray", width=[w / 100 for w in edge_weights], alpha=0.6)
# plt.title("MultiGraph: Genre Co-occurrences Over Years")

# plt.show()

# # Draw Simplified Graph (G) with Betweenness Centrality
# plt.figure(figsize=(12, 12))
# pos = nx.spring_layout(G, seed=42)
# node_sizes = [5000 * betweenness[n] for n in G.nodes()]
# edge_weights = [d["weight"] for _, _, d in G.edges(data=True)]
# nx.draw(G, pos, with_labels=True, node_color="lightcoral", edge_color="black", width=[w / 1000 for w in edge_weights], node_size=node_sizes, alpha=0.7)
# plt.title("Simplified Graph: Betweenness Centrality")

# plt.show()
