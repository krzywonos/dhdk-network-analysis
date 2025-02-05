import pandas as pd
from util import csv_to_multigraph, decade_graphs
import os

MG = csv_to_multigraph('genre_cooccurrences_in_a_year.csv', 'weight', 'label')
data = pd.read_csv("genre_cooccurrences_in_a_year.csv")
graphs_by_decade = decade_graphs(data, timestamp_label="release_year", weight_label="count")

# Weighted degree measure
degree_rank = dict()

for node in MG.nodes():
    degree_rank[node] = MG.degree[node]

top_degree = dict(sorted(degree_rank.items(), key=lambda item: item[1], reverse=True))
top_degree_df = pd.DataFrame(top_degree.items(), columns=['Genre', 'Degree'])
top_degree_df.index += 1

print(top_degree_df.to_string())

os.mkdir("measures_data/degree_by_decade")
for dec, g in graphs_by_decade.items():
    degree_rank = dict()

    for node in g.nodes():
        degree_rank[node] = g.degree[node]

    top_degree = dict(sorted(degree_rank.items(), key=lambda item: item[1], reverse=True))
    top_degree_df = pd.DataFrame(top_degree.items(), columns=['Genre', 'Degree'])
    top_degree_df.index += 1

    top_degree_df.to_csv(f"measures_data/degree_by_decade/{dec}_b.csv", index_label="Index")

