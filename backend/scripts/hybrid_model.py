#hybrid_model.py
import pandas as pd
from .utils import load_movies_data, load_ratings_data
from .similarity_model import get_similar_movies

movies = load_movies_data()
ratings = load_ratings_data()

def collaborative_recommend(title, top_n=10):

    movie_id = movies[movies['title'] == title]['movieId']

    if movie_id.empty:
        return []

    movie_id = movie_id.values[0]

    movie_ratings = ratings[ratings['movieId'] == movie_id]

    users = movie_ratings['userId'].unique()

    similar_movies = ratings[ratings['userId'].isin(users)]

    movie_scores = similar_movies.groupby('movieId')['rating'].mean()

    movie_scores = movie_scores.sort_values(ascending=False)

    recommended_ids = movie_scores.index.tolist()

    titles = movies[movies['movieId'].isin(recommended_ids)]['title'].tolist()

    return titles[:top_n]


def hybrid_recommend(title, top_n=10):

    content_movies = get_similar_movies(title, top_n)

    collab_movies = collaborative_recommend(title, top_n)

    combined = list(dict.fromkeys(content_movies + collab_movies))

    return combined[:top_n]