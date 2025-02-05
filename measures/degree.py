import pandas as pd
from util import csv_to_multigraph

MG = csv_to_multigraph('../data/genre_cooccurrences_in_a_year.csv', 'weight', 'label')

# Weighted degree measure
degree_rank = dict()

for node in MG.nodes():
    degree_rank[node] = MG.degree[node]

top_degree = dict(sorted(degree_rank.items(), key=lambda item: item[1], reverse=True))
top_degree_df = pd.DataFrame(top_degree.items(), columns=['Genre', 'Degree'])
top_degree_df.index += 1

print(top_degree_df.to_string())
