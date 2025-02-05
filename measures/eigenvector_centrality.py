import networkx as nx
from util import csv_to_multigraph, MG_to_G, decade_graphs
import pandas as pd
import os

MG = csv_to_multigraph('genre_cooccurrences_in_a_year.csv', 'weight', 'label')
G = MG_to_G(MG, 'weight')
data = pd.read_csv("genre_cooccurrences_in_a_year.csv")
graphs_by_decade = decade_graphs(data, timestamp_label="release_year", weight_label="count")

centrality = nx.eigenvector_centrality(G, weight='weight')
descending_dict = dict(sorted(centrality.items(), key=lambda item: item[1], reverse=True))
centrality_df = pd.DataFrame(descending_dict.items(), columns=['Genre', 'Centrality'])
centrality_df.index += 1

print(centrality_df.to_string())

os.mkdir('measures_data/eigenvector_by_decade')
for dec, g in graphs_by_decade.items():
    centrality = nx.eigenvector_centrality(g, weight='weight')
    descending_dict = dict(sorted(centrality.items(), key=lambda item: item[1], reverse=True))
    centrality_df = pd.DataFrame(descending_dict.items(), columns=['Genre', 'Centrality'])
    centrality_df.index += 1
    centrality_df.to_csv(f'measures_data/eigenvector_by_decade/{dec}_c.csv', index_label="Index")
