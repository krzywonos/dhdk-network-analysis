import networkx as nx
import os
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
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
    fig = plt.figure(figsize=(12, 12))
    fig.canvas.manager.set_window_title(f"{decade}: Betweenness Centrality")
    pos = nx.spring_layout(graph, seed=42)
    node_sizes = [5000 * betweenness[n] for n in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_color="lightcoral", edge_color="black", node_size=node_sizes, alpha=0.7)
    fig.suptitle(f"{decade}: Betweenness Centrality", fontsize=16)
    file_name = f"{decade}bc.png"
    output_dir = "./plots/bc"
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(fname=os.path.join(output_dir, file_name), dpi=300, bbox_inches="tight")

bc_df = pd.DataFrame(b_centralities, index=graphs_by_decade.keys())
bc_df = bc_df.apply(lambda x: round(x, ndigits=2))
measure_data_dir = "measures/measures_data"
os.makedirs(measure_data_dir, exist_ok=True)
path = os.path.join(measure_data_dir, "bc_by_dec.csv")
bc_df.to_csv(path_or_buf=path)
print(bc_df)