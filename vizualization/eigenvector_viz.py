from pyvis.network import Network
import networkx as nx
import pandas as pd
import os

cooccurrence_data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")

cooccurrence_data["decade"] = (cooccurrence_data["release_year"] // 10 * 10).astype(str) + "s"

output_dir = "eigenvector_centrality_by_decade"
os.makedirs(output_dir, exist_ok=True)

color_palette = ["#FF0000", "#FF4500", "#FFA500", "#FFD700", "#ADFF2F", "#32CD32", "#008000", "#006400"]

# unique decades 
decades = cooccurrence_data["decade"].unique()

for decade in decades:
    print(f"Generating Eigenvector Centrality Network for {decade}...")

    G = nx.Graph()
    filtered_data = cooccurrence_data[cooccurrence_data["decade"] == decade]

    for _, row in filtered_data.iterrows():
        genre1, genre2, weight = row["genre_1"], row["genre_2"], row["count"]
        G.add_edge(genre1, genre2, weight=weight)

    if G.number_of_nodes() == 0:
        print(f"Skipping {decade}, no data available.")
        continue

    eigenvector_centrality = nx.eigenvector_centrality(G, weight="weight", max_iter=1000)

    # normalizing centrality values
    max_eigen = max(eigenvector_centrality.values()) if eigenvector_centrality else 1

    # network
    net = Network(height="1200px", width="100%", notebook=True, bgcolor="#222222", font_color="white")
    net.barnes_hut(gravity=0, central_gravity=0, damping=1)  

    for node, centrality_value in eigenvector_centrality.items():
        size = 10 + (centrality_value / max_eigen) * 50
        color_index = int((centrality_value / max_eigen) * (len(color_palette) - 1))
        color = color_palette[color_index]

        net.add_node(node, label=node, color=color, size=size, title=f"Eigenvector Centrality: {centrality_value:.4f}")

    for u, v, data in G.edges(data=True):
        weight = data["weight"]
        edge_width = max(0.5, weight / 10)
        net.add_edge(u, v, color="gray", width=edge_width)

    file_name = f"{output_dir}/eigenvector_centrality_{decade}.html"
    net.save_graph(file_name)

    with open(file_name, "r", encoding="utf-8") as f:
        html_content = f.read()

    title_html = f"<h1 style='text-align:center; color:black;'>Eigenvector Centrality for {decade}</h1>"
    html_content = html_content.replace("<body>", f"<body>{title_html}", 1)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)

