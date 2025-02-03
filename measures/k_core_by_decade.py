import networkx as nx
import os
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint as pp
from statistics import median
from util import decade_graphs

# Compute k-cores based on weights
def weighted_decade_kcore(g:nx.Graph) -> dict:

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

if __name__ == "__main__":
    data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")
    graphs_by_decade = decade_graphs(data, timestamp_label="release_year", weight_label="count")
    decade_kcores = {decade: weighted_decade_kcore(graph) for decade, graph in graphs_by_decade.items()}
    pp(decade_kcores)