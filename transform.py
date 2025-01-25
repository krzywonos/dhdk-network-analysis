import csv
import ast
from collections import Counter
from itertools import combinations

genre_cooccurrences = Counter();
movie_genre_links = [];

with open("data/movies_metadata.csv", encoding="utf-8",errors="replace") as csvfile:
    reader = csv.DictReader(csvfile);
    for row in reader:
        genres = ast.literal_eval(row["genres"]);
        genre_names = [genre["name"].replace(" ", "_") for genre in genres];
        for genre_1, genre_2 in combinations(sorted(genre_names), 2):
            genre_cooccurrences[(genre_1, genre_2)] += 1;
        movie_id = row["imdb_id"];
        for genre in genre_names:
            movie_genre_links.append((movie_id, genre))

with open('data/genre_cooccurrences.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['genre_1', 'genre_2', 'count'])
    for (genre_1, genre_2), count in genre_cooccurrences.items():
        writer.writerow([genre_1, genre_2, count])

with open('data/movie_genre_links.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['movie', 'genre'])
    for movie, genre in movie_genre_links:
        writer.writerow([movie, genre])