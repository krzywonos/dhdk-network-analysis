from pyvis.network import Network
import networkx as nx
import pandas as pd
import os

# Load genre co-occurrence data with proper encoding handling
cooccurrence_data = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")

# Convert release year to decade format
cooccurrence_data["decade"] = (cooccurrence_data["release_year"] // 10 * 10).astype(str) + "s"

# Create output directory if it does not exist
output_dir = "k_core_by_decade"
os.makedirs(output_dir, exist_ok=True)

# Get unique decades
decades = cooccurrence_data["decade"].unique()

for decade in decades:
    print(f"Generating K-Core Network for {decade}...")

    # Create a graph for this decade
    G = nx.Graph()
    filtered_data = cooccurrence_data[cooccurrence_data["decade"] == decade]

    # Add edges with weights
    for _, row in filtered_data.iterrows():
        genre1, genre2, weight = row["genre_1"], row["genre_2"], row["count"]
        G.add_edge(genre1, genre2, weight=weight)

    # Extract K-Core
    if G.number_of_nodes() == 0:
        print(f"Skipping {decade}, no data available.")
        continue

    k_core_graph = nx.k_core(G)

    # PyVis network with static layout
    net = Network(height="1200px", width="100%", notebook=True, bgcolor="#222222", font_color="white")

    # Use a fixed layout to keep positions stable across different decades
    pos = nx.spring_layout(k_core_graph, seed=42)

    # Compute node sizes dynamically based on degree centrality
    degree_centrality = nx.degree_centrality(k_core_graph)

    # Add nodes with sizes based on degree centrality
    for node in k_core_graph.nodes():
        x, y = pos[node]
        size = 10 + degree_centrality[node] * 50  # Scale size dynamically
        net.add_node(node, label=node, color="violet", size=size, x=x*1000, y=y*1000)

    # Add edges
    for u, v in k_core_graph.edges():
        net.add_edge(u, v, color="gray", width=1.5)

    # Disable physics for a static layout
    net.toggle_physics(False)

    # Save as HTML
    file_name = f"{output_dir}/k_core_{decade}.html"
    net.save_graph(file_name)

    # Add a title to the HTML file
    with open(file_name, "r", encoding="utf-8") as f:
        html_content = f.read()

    title_html = f"<h1 style='text-align:center; color:black;'>K-Core network for {decade}</h1>"
    html_content = html_content.replace("<body>", f"<body>{title_html}", 1)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)

print("✅ All K-Core Networks saved as static HTML files!")
