import networkx as nx
from util import csv_to_multigraph, MG_to_G
import pandas as pd

MG = csv_to_multigraph('genre_cooccurrences_in_a_year.csv', 'weight', 'label')
G = MG_to_G(MG, 'weight')

centrality = nx.eigenvector_centrality(G, weight='weight')
descending_dict = dict(sorted(centrality.items(), key=lambda item: item[1], reverse=True))
centrality_df = pd.DataFrame(descending_dict.items(), columns=['Genre', 'Centrality'])
centrality_df.index += 1

print(centrality_df.to_string())