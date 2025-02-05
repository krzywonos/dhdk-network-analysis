import networkx as nx
import pandas as pd

def df_to_graph(data:pd.DataFrame, weights:str, label:str) -> nx.Graph:
    # Graph representing our dataset
    G = nx.Graph()

    for _,row in data.iterrows():
        u = row.iloc[0]
        v = row.iloc[1]
        if G.has_edge(u, v):
            G[u][v]["weight"] += row[weights]
            G[u][v]["year"].append(row[label])
        else:
            G.add_edge(u, v, weight=row[weights], year=[row[label]])
    return G

def decade_graphs (data: pd.DataFrame, timestamp_label:str, weight_label: str) -> dict[str : nx.Graph]:

    data["decade"] = data[timestamp_label].apply(lambda x: str(x)[0:3] + "0s")
    data_by_decade = data.groupby("decade", group_keys=False)

    graphs_by_decade = {}
    for decade, df in data_by_decade:
        graph = nx.Graph()
        for _, row in df.iterrows():
            u = row.iloc[0]
            v = row.iloc[1]
            if graph.has_edge(u, v):
                graph[u][v]["weight"] += row[weight_label]
                graph[u][v]["year"].append(row[timestamp_label])
            else:
                graph.add_edge(u, v, year=[row[timestamp_label]], weight=row[weight_label])
        graphs_by_decade[decade] = graph

    return graphs_by_decade

def csv_to_multigraph(csv_file, weights:str, label:str) -> nx.MultiGraph:
    # csv_file must be a csv file path
    try:
        os.path.isfile(csv_file) and csv_file.endswith(".csv")
    except:
        print("\'csv_file\' must be a csv file path, check its correctness.")
        
    # Loading csv file in read mode
    data = open(csv_file, "r")
    next(data, None) # Skipping headers

    # Multigraph representing our dataset
    MG = nx.parse_edgelist(data, delimiter=',', create_using=nx.MultiGraph(), nodetype=str, data=((label, int),(weights, int),))

    return MG

def MG_to_G(multigraph:nx.MultiGraph, weight:str) -> nx.Graph:
    G = nx.Graph()

    # Weights aggregation
    for u, v, data in multigraph.edges(data=True):
        if G.has_edge(u, v):
            G[u][v][weight] += data[weight]  # Sum weights
        else:
            G.add_edge(u, v, weight=data[weight])

    return G
