from pyvis.network import Network
import networkx as nx
import pandas as pd
import os

cooccurrence_data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")

cooccurrence_data["decade"] = (cooccurrence_data["release_year"] // 10 * 10).astype(str) + "s"

output_dir = "k_core_by_decade"
os.makedirs(output_dir, exist_ok=True)

decades = cooccurrence_data["decade"].unique()

for decade in decades:
    print(f"Generating K-Core Network for {decade}...")

    # a graph for this decade
    G = nx.Graph()
    filtered_data = cooccurrence_data[cooccurrence_data["decade"] == decade]

    # edges with weights
    for _, row in filtered_data.iterrows():
        genre1, genre2, weight = row["genre_1"], row["genre_2"], row["count"]
        G.add_edge(genre1, genre2, weight=weight)

    # extracting K-Core 
    if G.number_of_nodes() == 0:
        print(f"Skipping {decade}, no data available.")
        continue

    k_core_graph = nx.k_core(G)

    # PyVis network
    net = Network(height="800px", width="100%", notebook=True, bgcolor="#222222", font_color="white")

    # adding nodes 
    for node in k_core_graph.nodes():
        net.add_node(node, label=node, color="violet", size=15)

    # adding edges
    for u, v in k_core_graph.edges():
        net.add_edge(u, v, color="gray", width=1.5)

    # saving
    file_name = f"{output_dir}/k_core_{decade}.html"
    net.save_graph(file_name)

    with open(file_name, "r", encoding="utf-8") as f:
        html_content = f.read()

    title_html = f"<h1 style='text-align:center; color:black;'>K-Core Network for {decade}</h1>"
    html_content = html_content.replace("<body>", f"<body>{title_html}", 1)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)
