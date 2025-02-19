import pandas as pd
import ast
import plotly.express as px

louvian_modularity_df = pd.read_csv("measures/measures_data/Louvian_Modularity_by_decades.csv", index_col=0)

df_list = []
for decade, row in louvian_modularity_df.iterrows():
    communities = ast.literal_eval(row["Communities"])
    for i, community in enumerate(communities):
        for genre in community:
            df_list.append({"Decade": decade, "Community": f"C{i}", "Genre": genre})

df_alluvial = pd.DataFrame(df_list)

fig = px.parallel_categories(df_alluvial, dimensions=["Decade", "Community", "Genre"],
                             title="Louvain modularity")
fig.show()
