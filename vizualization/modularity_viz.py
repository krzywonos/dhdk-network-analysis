from pyvis.network import Network
import networkx as nx
import pandas as pd
import os
import re 

modularity_data = pd.read_csv("measures/measures_data/Greedy_Modularity_by_decades.csv")

def parse_communities(community_string):
    try:
        cleaned_string = re.sub(r'frozenset\((.*?)\)', r'\1', community_string)

        communities = eval(cleaned_string)

        # communities are lists of genres
        parsed_communities = []
        for community in communities:
            if isinstance(community, set):  
                parsed_communities.append(list(community))
            elif isinstance(community, list): 
                parsed_communities.append(community)

        return parsed_communities
    except Exception as e:
        print(f"Skipping malformed data: {community_string}, Error: {e}")
        return []  
    
modularity_data["Communities"] = modularity_data["Communities"].apply(parse_communities)

output_dir = "greedy_modularity_by_decade"
os.makedirs(output_dir, exist_ok=True)

color_palette = ["#E6194B", "#3CB44B", "#FFE119", "#4363D8", "#F58231", "#911EB4",
                 "#46F0F0", "#F032E6", "#9A6324", "#469990", "#800000", "#808000",
                 "#000075", "#A9A9A9", "#FFD700", "#FF69B4", "#D2691E", "#DC143C"]

# looping
for index, row in modularity_data.iterrows():
    decade = row["Decades"]
    communities = row["Communities"]
    modularity_score = row["Modularity"]

    print(f"Decade: {decade}, Extracted Communities: {communities}")

    # skip if there is no valid community data
    if not communities or all(len(c) == 0 for c in communities):
        print(f"Skipping {decade}, no valid community data.")
        continue

    print(f"Generating Greedy Modularity Network for {decade}...")

    G = nx.Graph()

    modularity_class = {}
    for i, community in enumerate(communities):
        for genre in community:
            modularity_class[genre] = i

    net = Network(height="1200px", width="100%", notebook=True, bgcolor="#222222", font_color="white")

    for genre, community_id in modularity_class.items():
        color = color_palette[community_id % len(color_palette)]
        net.add_node(genre, label=genre, color=color, size=15)

    for community in communities:
        for genre1 in community:
            for genre2 in community:
                if genre1 != genre2:
                    G.add_edge(genre1, genre2)

    for u, v in G.edges():
        net.add_edge(u, v, color="gray", width=1.5)

    file_name = f"{output_dir}/greedy_modularity_{decade}.html"
    net.save_graph(file_name)

    with open(file_name, "r", encoding="utf-8") as f:
        html_content = f.read()

    title_html = f"<h1 style='text-align:center; color:black;'>Greedy Modularity Network for {decade}<br>Modularity Score: {modularity_score:.4f}</h1>"
    html_content = html_content.replace("<body>", f"<body>{title_html}", 1)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)
