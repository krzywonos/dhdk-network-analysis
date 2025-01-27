import csv
import ast
from collections import Counter
from itertools import combinations

genre_cooccurrences = Counter();
genre_year_combinations = [];
genre_cooccurrences_in_a_year = Counter();

with open("data/movies_metadata.csv", encoding="utf-8",errors="replace") as csvfile:
    reader = csv.DictReader(csvfile);
    for row in reader:
        genres = ast.literal_eval(row["genres"]);
        genre_names = [genre["name"].replace(" ", "_") for genre in genres];
        for genre_1, genre_2 in combinations(sorted(genre_names), 2): #2-genre combinations
            genre_cooccurrences[(genre_1, genre_2)] += 1;
        release_date = row.get('release_date', '');
        release_year = release_date[:4] if release_date and release_date[:4].isdigit() else None;
        if release_year:
            for genre_1, genre_2 in combinations(sorted(genre_names), 2): #2-genre combinations
                genre_year_combinations.append((genre_1, genre_2, release_year));
                genre_cooccurrences_in_a_year[(genre_1, genre_2, release_year)] += 1

with open('data/genre_cooccurrences.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file);
    writer.writerow(['genre_1', 'genre_2', 'count']);
    for (genre_1, genre_2), count in genre_cooccurrences.items():
        writer.writerow([genre_1, genre_2, count]);

with open('data/genre_cooccurences_years.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file);
    writer.writerow(['genre_1', 'genre_2', 'release_year']);
    for genre_1, genre_2, year in genre_year_combinations:
        writer.writerow([genre_1, genre_2, year]);

with open('data/genre_cooccurrences_in_a_year.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['genre_1', 'genre_2', 'release_year', 'count'])
    for (genre_1, genre_2, year), count in genre_cooccurrences_in_a_year.items():
        writer.writerow([genre_1, genre_2, year, count])