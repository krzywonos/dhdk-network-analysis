import networkx as nx
from networkx.algorithms.community import quality as nx_quality
from networkx.algorithms.community import louvain_communities
from util import csv_to_multigraph, MG_to_G, decade_graphs
import pandas as pd
import os

MG = csv_to_multigraph('../data/genre_cooccurrences_in_a_year.csv', 'weight', 'label')
G = MG_to_G(MG, 'weight')
data = pd.read_csv("../data/genre_cooccurrences_in_a_year.csv")
graphs_by_decade = decade_graphs(data, timestamp_label="release_year", weight_label="count")

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

d_greedy_modularity = dict()
d_louvian_modularity = dict()
os.mkdir("measures_data/modularity")
# Same measures, but for each decade
for decade, graph in graphs_by_decade.items():
    d_communities = nx.community.greedy_modularity_communities(graph)
    d_Q1 = nx_quality.modularity(graph, d_communities)
    d_greedy_modularity[decade] = (d_communities, d_Q1)
    d_louvian_comm = louvain_communities(graph)
    d_Q2 = nx_quality.modularity(graph, d_louvian_comm)
    d_louvian_modularity[decade] = (d_louvian_comm, d_Q2)
df_greedy = pd.DataFrame(d_greedy_modularity.values(), d_greedy_modularity.keys(), columns=["Communities", "Modularity"])
df_louvian = pd.DataFrame(d_louvian_modularity.values(), d_louvian_modularity.keys(), columns=["Communities", "Modularity"])
df_greedy.to_csv("measures_data/modularity/Greedy_Modularity_by_decades.csv", ",", index_label="Decades")
df_louvian.to_csv("measures_data/modularity/Louvian_Modularity_by_decades.csv", ",", index_label="Decades")
