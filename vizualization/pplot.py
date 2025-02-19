import pandas as pd
import matplotlib.pyplot as plt

bc_by_dec = pd.read_csv("measures/measures_data/bc_by_dec.csv", index_col=0)

bc_by_dec.index = bc_by_dec.index.astype(str)

#top 10 genres with the highest average betweenness centrality
top_genres = bc_by_dec.mean().nlargest(10).index

# Select only these top genres
bc_top_genres = bc_by_dec[top_genres]

# Create the time series plot
plt.figure(figsize=(12, 6))
for genre in bc_top_genres.columns:
    plt.plot(bc_top_genres.index, bc_top_genres[genre], marker='o', linestyle='-', label=genre)

plt.xlabel("Decade")
plt.ylabel("Betweenness centrality")
plt.title("Evolution of betweenness centrality over time for top genres")
plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1))
plt.grid(True)

# Save the plot
plt.savefig("betweenness_time_series.png", dpi=300, bbox_inches="tight")

# Show plot
plt.show()



