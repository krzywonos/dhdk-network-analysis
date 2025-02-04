import networkx as nx
import os
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint as pp
from statistics import median, mean
from typing import Optional
from util import df_to_graph

# Compute k-cores based on weights
def weighted_kcore(g:nx.Graph, k: Optional[int] = None) -> list:
    
    graph = g.copy()
    weighted_degrees = {node: deg 
                        for node, deg in nx.degree(graph, weight="weight")}
    if not k:
        k = round(median(sorted(weighted_degrees.values()))) 

    nodes_to_remove = [node for node, deg in weighted_degrees.items()
                        if deg < k]
    
    while nodes_to_remove:
        graph.remove_nodes_from(nodes_to_remove)

        weighted_degrees = {node: deg 
                            for node, deg in nx.degree(graph, weight="weight")}
        
        nodes_to_remove = [node 
                           for node, deg in weighted_degrees.items()
                           if deg < k]
        
    k_nodes = list(graph.nodes())

    print(f"K value: {k}", f"Nodes: {len(k_nodes)}")
    return k_nodes

def kcore_by_len(G: nx.Graph, initial_k, target_len: int):

    k = initial_k
    degrees = [val for _, val in nx.degree(G=G, weight="weight")]
    ceiling = max(degrees)
    k_core = weighted_kcore(G, k=k)

    while k <= ceiling:
        if len(k_core) < target_len:
            return []
        elif len(k_core) == target_len:
            break
        k += 1
        k_core = weighted_kcore(G, k=k)

    return k_core

if __name__ == "__main__":
    data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")
    graph = df_to_graph(data, weights="count", label="release_year")
    print(kcore_by_len(graph, initial_k=0, target_len=2))



