import pandas as pd

# Load datasets
movies = pd.read_csv("backend/data/movies.csv")
ratings = pd.read_csv("backend/data/ratings.csv")
tags = pd.read_csv("backend/data/tags.csv")
links = pd.read_csv("backend/data/links.csv")

# Show first few rows
print("Movies Dataset")
print(movies.head())

print("\nRatings Dataset")
print(ratings.head())

print("\nTags Dataset")
print(tags.head())