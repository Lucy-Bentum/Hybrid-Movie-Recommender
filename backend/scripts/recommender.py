import pandas as pd
import os
from dotenv import load_dotenv
from .utils import (
    load_movies_data,
    load_ratings_data,
    load_tags_data,
    fuzzy_search,
    get_movie_poster,
    rating_to_stars,
    get_movie_trailer
)
from .hybrid_model import hybrid_recommend

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# ------------------------
# Load datasets once
# ------------------------
movies = load_movies_data()
ratings = load_ratings_data()
tags = load_tags_data()


# ------------------------
# Get hybrid recommendations
# ------------------------
def get_recommendations(user_input, top_n=10):
    """
    Returns top_n recommended movies for a given user_input.
    Each movie includes: title, poster_url, trailer, avg_rating, stars, genres, score, popularity
    """
    movie_titles = movies['title'].tolist()

    matched = fuzzy_search(user_input, movie_titles, limit=1)
    if not matched:
        return []

    main_movie = matched[0]

    hybrid_movies = hybrid_recommend(main_movie, top_n)

    titles = [main_movie] + hybrid_movies

    recommendations = []

    for title in titles:
        # Poster & trailer
        poster = get_movie_poster(title, TMDB_API_KEY)
        trailer = get_movie_trailer(title, TMDB_API_KEY)

        # Ratings
        movie_row = movies[movies['title'] == title]
        if movie_row.empty:
            continue

        movie_id = movie_row['movieId'].values[0]
        movie_ratings = ratings[ratings['movieId'] == movie_id]['rating']

        avg_rating = movie_ratings.mean() if not movie_ratings.empty else 0
        popularity = len(movie_ratings)  # Number of ratings = popularity

        # Hybrid score
        score = (avg_rating * 0.7) + (popularity * 0.3)

        stars = rating_to_stars(avg_rating)
        genres = movie_row['genres'].values[0]

        recommendations.append({
            "title": title,
            "poster_url": poster,
            "trailer": trailer,
            "avg_rating": avg_rating,
            "stars": stars,
            "genres": genres,
            "score": score,
            "popularity": popularity
        })

    # ------------------------
    # Sort by hybrid score
    # ------------------------
    recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)

    # ------------------------
    # Ensure searched movie appears first
    # ------------------------
    main_movie_data = None

    for movie in recommendations:
        if movie["title"] == main_movie:
            main_movie_data = movie
            break

    if main_movie_data:
        recommendations = [m for m in recommendations if m["title"] != main_movie]
        recommendations.insert(0, main_movie_data)

    return recommendations[:top_n]