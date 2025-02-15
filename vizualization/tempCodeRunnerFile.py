def parse_communities(community_string):
    try:
        # Remove unwanted characters
        cleaned_string = re.sub(r'[{]|[}]', '', community_string)  # Remove curly brackets
        cleaned_string = cleaned_string.replace("'", "")  # Remove single quotes
        
        # Split by "], [" to separate communities
        communities = [community.split(", ") for community in cleaned_string.split("], [")]

        return communities
    except:
        return []  # Return an empty list if parsing fails

# Apply the function to parse the "Communities" column
modularity_data["Communities"] = modularity_data["Communities"].apply(parse_communities)

# Create a folder to save the graphs
output_dir = "louvain_modularity_by_decade"
os.makedirs(output_dir, exist_ok=True)

# Define a modern aesthetic color palette for communities
color_palette = ["#E63946", "#52B788", "#457B9D", "#F4A261", "#9B5DE5",
                 "#FF9F1C", "#2A9D8F", "#E76F51", "#7B2CBF", "#6D6875"]

# Loop through each decade
for index, row in modularity_data.iterrows():
    decade = row["Decades"]
    communities = row["Communities"]
    modularity_score = row["Modularity"]

    # Debugging: Print extracted communities
    print(f"Decade: {decade}, Extracted Communities: {communities}")

    # Skip if there is no valid community data
    if not communities or all(len(c) == 0 for c in communities):
        print(f"Skipping {decade}, no valid community data.")
        continue

    print(f"Generating Louvain Modularity Network for {decade}...")

    # Create a graph
    G = nx.Graph()

    # Assign a community ID to each genre
    modularity_class = {}
    for i, community in enumerate(communities):
        for genre in community:
            modularity_class[genre] = i

    # Create a PyVis network (STATIC: physics disabled)
    net = Network(height="1200px", width="100%", notebook=True, bgcolor="#1E1E1E", font_color="white")
    net.barnes_hut(gravity=0, central_gravity=0, damping=1)  # Disable physics for static layout

    # Add nodes with colors based on community
    for genre, community_id in modularity_class.items():
        color = color_palette[community_id % len(color_palette)]
        net.add_node(genre, label=genre, color=color, size=15)

    # Connect genres within each community
    for community in communities:
        for genre1 in community:
            for genre2 in community:
                if genre1 != genre2:
                    G.add_edge(genre1, genre2)

    # Add edges to the visualization
    for u, v in G.edges():
        net.add_edge(u, v, color="gray", width=1.5)

    # Save the graph
    file_name = f"{output_dir}/louvain_modularity_{decade}.html"
    net.save_graph(file_name)

    # Modify the HTML file to insert the correct title with modularity score
    with open(file_name, "r", encoding="utf-8") as f:
        html_content = f.read()

    title_html = f"<h1 style='text-align:center; color:black;'>Louvain Modularity Network for {decade}<br>Modularity Score: {modularity_score:.4f}</h1>"
    html_content = html_content.replace("<body>", f"<body>{title_html}", 1)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)

print("✅ All Louvain Modularity by Decade networks saved! Networks are now STATIC with a modern color palette.")
