import networkx as nx
from networkx.algorithms.community import quality as nx_quality
from networkx.algorithms.community import louvain_communities
from util import csv_to_multigraph, MG_to_G
import pandas as pd

MG = csv_to_multigraph('../data/genre_cooccurrences_in_a_year.csv', 'weight', 'label')
G = MG_to_G(MG, 'weight')

# Modularity measure done using different techniques to generate communities

# Greedy Modularity Algorithm
communities = nx.community.greedy_modularity_communities(MG)
print("\n\nDetected communities using Greedy Modularity Algorithm:")
for _ in communities:
    print(_)

Q1 = nx_quality.modularity(MG, communities)
print("\n\nModularity Q1:", Q1)

# Louvain Community Detection Algorithm
louvain_comm = louvain_communities(G)
print("\n\nDetected communities using Louvain Community Detection Algorithm:")
for _ in louvain_comm:
    print(_)

Q2 = nx_quality.modularity(MG, louvain_comm)
print("\n\nModularity Q2:", Q2)
