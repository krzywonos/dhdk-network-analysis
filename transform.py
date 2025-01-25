import csv
import ast

genres = set()
with open("data/movies_metadata.csv", encoding="utf-8",errors="replace") as csvfile:
    reader = csv.DictReader(csvfile);
    for row in reader:
        row_genres = ast.literal_eval(row["genres"]);
        for genre in row_genres:
            genres.add((genre["id"], genre["name"]));

genres_list = sorted(genres, key=lambda x: x[0]);
print(genres_list)

genre_names = [name for _, name in genres_list]
print(genre_names)