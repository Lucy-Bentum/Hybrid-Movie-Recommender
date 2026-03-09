import pandas as pd
import os
from dotenv import load_dotenv
import requests
from fuzzywuzzy import process

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# ------------------------
# Load datasets
# ------------------------
def load_movies_data(data_path="backend/data/movies.csv"):
    return pd.read_csv(data_path)

def load_ratings_data(data_path="backend/data/ratings.csv"):
    return pd.read_csv(data_path)

def load_tags_data(data_path="backend/data/tags.csv"):
    return pd.read_csv(data_path)

# ------------------------
# Fuzzy search
# ------------------------
def fuzzy_search(query, choices, limit=10):
    results = process.extract(query, choices, limit=limit)
    return [title for title, score in results]

# ------------------------
# Clean movie title
# ------------------------
def clean_title(title):
    if "(" in title:
        return title.split("(")[0].strip()
    return title

# ------------------------
# Poster
# ------------------------
def get_movie_poster(title, api_key):
    try:
        title = clean_title(title)
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
        response = requests.get(url).json()
        if response.get("results"):
            poster_path = response["results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception as e:
        print(e)
    return "https://via.placeholder.com/500x750?text=Poster+Unavailable"

# ------------------------
# Trailer
# ------------------------
def get_movie_trailer(title, api_key):
    try:
        title = clean_title(title)
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
        data = requests.get(search_url).json()
        if not data["results"]:
            return None
        movie_id = data["results"][0]["id"]
        video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
        videos = requests.get(video_url).json()
        for vid in videos["results"]:
            if vid["type"] == "Trailer" and vid["site"] == "YouTube":
                return f"https://www.youtube.com/watch?v={vid['key']}"
    except:
        return None
    return None

# ------------------------
# Stars
# ------------------------
def rating_to_stars(rating):
    if pd.isna(rating):
        return "No rating"
    stars_count = int(round(rating))
    return "⭐" * stars_count

# ------------------------
# Recent Movies
# ------------------------
def get_recent_movies(year=2026, top_n=10):
    url = f"https://api.themoviedb.org/3/discover/movie?primary_release_year={year}&api_key={TMDB_API_KEY}"
    response = requests.get(url).json()

    movies_list = []

    for movie in response.get("results", [])[:top_n]:
        title = movie["title"]
        poster = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
        movie_id = movie["id"]

        # Trailer
        video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
        videos = requests.get(video_url).json()
        trailer = None
        for vid in videos.get("results", []):
            if vid["type"] == "Trailer" and vid["site"] == "YouTube":
                trailer = f"https://www.youtube.com/watch?v={vid['key']}"
                break

        movies_list.append({
            "title": title,
            "poster": poster,
            "trailer": trailer,
            "avg_rating": 0,
            "stars": "",
            "genres": ""
        })

    return movies_list

# ------------------------
# Trending Movies
# ------------------------
def get_trending_movies(top_n=10):
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    response = requests.get(url).json()

    movies_list = []

    for movie in response.get("results", [])[:top_n]:
        title = movie["title"]
        poster = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
        movie_id = movie["id"]

        # Trailer
        video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
        videos = requests.get(video_url).json()
        trailer = None
        for vid in videos.get("results", []):
            if vid["type"] == "Trailer" and vid["site"] == "YouTube":
                trailer = f"https://www.youtube.com/watch?v={vid['key']}"
                break

        movies_list.append({
            "title": title,
            "poster": poster,
            "trailer": trailer,
            "avg_rating": 0,
            "stars": "",
            "genres": ""
        })

    return movies_list
