import networkx as nx
import os
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint as pp
from statistics import median, mean
from typing import Optional
from util import df_to_graph

# Compute k-cores based on weights
def weighted_kcore(g:nx.Graph, k: Optional[int] = None) -> dict[tuple:list[str]]:

    weighted_degrees = {node: sum(d["weight"] for _, _, d in g.edges(node, data=True)) for node in g.nodes()}
    k = round(median(sorted(weighted_degrees.values()))) if not k else k

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

data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")
graph = df_to_graph(data, weights="count", label="release_year")
k_cores = weighted_kcore(graph)
pp(k_cores)