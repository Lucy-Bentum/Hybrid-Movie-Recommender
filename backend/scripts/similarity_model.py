#similarity_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .utils import load_movies_data, load_tags_data

movies = load_movies_data()
tags = load_tags_data()

# Merge tags
tags_grouped = tags.groupby('movieId')['tag'].apply(lambda x: " ".join(x)).reset_index()

movies = movies.merge(tags_grouped, on='movieId', how='left')
movies['tag'] = movies['tag'].fillna("")

# Combine text features
movies['content'] = movies['genres'] + " " + movies['tag']

tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(movies['content'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_similar_movies(title, top_n=10):

    idx = movies[movies['title'] == title].index

    if len(idx) == 0:
        return []

    idx = idx[0]

    scores = list(enumerate(cosine_sim[idx]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:top_n+1]

    movie_indices = [i[0] for i in scores]

    return movies.iloc[movie_indices]['title'].tolist()