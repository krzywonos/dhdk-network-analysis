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