from pyvis.network import Network
import networkx as nx
import pandas as pd
import os

bc_data = pd.read_csv("measures/measures_data/bc_by_dec.csv", index_col=0)  
cooccurrence_data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")

cooccurrence_data["decade"] = (cooccurrence_data["release_year"] // 10 * 10).astype(str) + "s"

# output directory
output_dir = "betweenness_by_decade"
os.makedirs(output_dir, exist_ok=True)

# Iterate through each decade in Betweenness Centrality Data
for decade in bc_data.index:
    print(f"Generating Betweenness Centrality Network for {decade}...")

    # Get betweenness values for this decade
    decade_betweenness = bc_data.loc[decade].dropna().to_dict()

    # If no data exists for the decade, skip
    if not decade_betweenness:
        print(f"Skipping {decade}, no betweenness data found.")
        continue

    # Get max betweenness 
    max_bc = max(decade_betweenness.values()) if max(decade_betweenness.values()) > 0 else 1
    filtered_data = cooccurrence_data[cooccurrence_data["decade"] == decade]

    # init graph
    G = nx.Graph()

    # adding edges
    for _, row in filtered_data.iterrows():
        genre1 = row["genre_1"]
        genre2 = row["genre_2"]
        weight = row["count"]
        G.add_edge(genre1, genre2, weight=weight)

    # PyVis network
    net = Network(height="800px", width="100%", notebook=True, bgcolor="#222222", font_color="white")

    # nodes with betweenness tooltip
    for node in G.nodes():
        bc_value = decade_betweenness.get(node, 0)  # betweenness value, or default to 0
        size = 10 + (bc_value / max_bc) * 50  # normalizing size
        color = "pink" if bc_value > 0.1 else "	#ADD8E6"

        net.add_node(
            node,
            label=node,
            color=color,
            size=size,
            title=f"Betweenness: {bc_value:.4f}" 
        )

    # edges
    for u, v, data in G.edges(data=True):
        weight = data["weight"]
        edge_width = max(0.5, weight / 10)  
        net.add_edge(u, v, color="gray", width=edge_width)

    file_name = f"{output_dir}/betweenness_{decade}.html"

    net.save_graph(file_name)

    with open(file_name, "r", encoding="utf-8") as f:
        html_content = f.read()

    title_html = f"<h1 style='text-align:center; color:black;'>Betweenness Centrality for {decade}</h1>"
    html_content = html_content.replace("<body>", f"<body>{title_html}", 1)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)

