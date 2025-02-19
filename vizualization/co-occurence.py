import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/genre_cooccurrences_in_a_year.csv")

df["decade"] = (df["release_year"] // 10) * 10

genre_cooccurrence_trends = df.groupby(["decade", "genre_1", "genre_2"])["count"].sum().reset_index()

top_genre_pairs = genre_cooccurrence_trends.groupby(["genre_1", "genre_2"])["count"].sum().nlargest(10).index

filtered_df = genre_cooccurrence_trends.set_index(["genre_1", "genre_2"]).loc[top_genre_pairs].reset_index()

plt.figure(figsize=(12, 6))
for (genre1, genre2), group in filtered_df.groupby(["genre_1", "genre_2"]):
    plt.plot(group["decade"], group["count"], marker="o", linestyle="-", label=f"{genre1} & {genre2}")

plt.title("Top 10 genre pairs with increasing co-occurrences over time")
plt.xlabel("Decades")
plt.ylabel("Co-occurrence count")
plt.legend(title="Genre pairs", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()
