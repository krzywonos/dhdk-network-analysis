import networkx as nx
import os
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint as pp
from statistics import median
from util import decade_graphs
from k_core import weighted_kcore



def main():
    data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")
    graphs_by_decade = decade_graphs(data, timestamp_label="release_year", weight_label="count")
    for decade, g in graphs_by_decade.items():
        k_core = weighted_kcore(g)
        meta, graph = list(k_core.keys())[0], list(k_core.values())[0]
        fig = plt.figure(figsize=(12, 12))
        fig.canvas.manager.set_window_title(f"{decade}: K-core {meta[0]}")
        pos = nx.spring_layout(graph, seed=42)
        edge_sizes = [data["weight"]*0.1 for _, _, data in graph.edges(data=True)]
        nx.draw(graph, pos, with_labels=True, node_color="lightcoral", edge_color="black", width=edge_sizes, alpha=0.7)
        fig.suptitle(f"{decade}: K-core {meta[0]}", fontsize=16)
        file_name = f"{decade}kc.png"
        output_dir = "./plots/kc"
        os.makedirs(output_dir, exist_ok=True)
        fig.savefig(fname=os.path.join(output_dir, file_name), dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    main()
