import sys
import os
# Add project root to path so Python can find backend.scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv

from backend.scripts.utils import (
    load_movies_data,
    load_ratings_data,
    get_recent_movies,
    get_trending_movies,
    get_movie_poster,
    get_movie_trailer
)
from backend.scripts.recommender import get_recommendations

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# ------------------------
# Page config
# ------------------------
st.set_page_config(
    page_title="Hybrid Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ------------------------
# Load CSS for styling
# ------------------------
with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------------
# Page title
# ------------------------
st.markdown("<h1 class='main-title'>🎬 Hybrid Movie Recommender</h1>", unsafe_allow_html=True)

# ------------------------
# Load movie & ratings data
# ------------------------
movies = load_movies_data()
ratings = load_ratings_data()
movie_titles = movies['title'].tolist()

# ------------------------
# Initialize search history
# ------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------
# Sidebar: Recently Searched
# ------------------------
st.sidebar.title("🕘 Recently Searched")
if st.session_state.history:
    for movie in st.session_state.history:
        if st.sidebar.button(movie, key=movie):
            search_input = movie

# ------------------------
# Search bar with autocomplete
# ------------------------
search_input = st.selectbox("Search movie", movie_titles)

if search_input:

    # Add to history
    if search_input not in st.session_state.history:
        st.session_state.history.insert(0, search_input)
        if len(st.session_state.history) > 5:
            st.session_state.history.pop()

    # ------------------------
    # Fetch all movie lists first
    # ------------------------
    recent_movies = get_recent_movies()
    trending_movies = get_trending_movies()

    # ------------------------
    # Display Recommendations (5 per row) WITH spinner
    # ------------------------
    with st.spinner("Fetching recommendations..."):
        recommended_movies = get_recommendations(search_input)

        st.markdown("<div class='recommend-header'>Top Recommendations For You</div>", unsafe_allow_html=True)

        for i in range(0, len(recommended_movies), 5):
            row_movies = recommended_movies[i:i+5]
            cols = st.columns(5)
            for idx, movie in enumerate(row_movies):
                with cols[idx]:
                    st.image(movie.get('poster_url',"https://via.placeholder.com/500x750?text=No+Image"), width=200)
                    st.subheader(movie['title'])
                    st.write(f"Rating: {movie['avg_rating']:.1f}")
                    st.write(movie['stars'])
                    st.write(f"Popularity Score: {movie.get('popularity',0)}")
                    if movie.get('genres'):
                        badges = " ".join([f"<span class='genre-badge'>{g}</span>" for g in movie['genres'].split("|")])
                        st.markdown(badges, unsafe_allow_html=True)
                    if movie.get("trailer"):
                        st.video(movie["trailer"])

    # ------------------------
    # Display Recent Movies (5 per row)
    # ------------------------
    st.markdown("## 🆕 Recent Movies")
    for i in range(0, len(recent_movies), 5):
        row_movies = recent_movies[i:i+5]
        cols = st.columns(5)
        for idx, movie in enumerate(row_movies):
            with cols[idx]:
                st.image(movie.get("poster"), width=200)
                st.subheader(movie['title'])
                st.write(f"Rating: {movie.get('avg_rating',0):.1f}")
                st.write(movie.get('stars',''))
                if movie.get('genres'):
                    badges = " ".join([f"<span class='genre-badge'>{g}</span>" for g in movie['genres'].split("|")])
                    st.markdown(badges, unsafe_allow_html=True)
                if movie.get("trailer"):
                    st.video(movie["trailer"])

    # ------------------------
    # Display Trending Movies (5 per row)
    # ------------------------
    st.markdown("## 🔥 Trending Movies")
    for i in range(0, len(trending_movies), 5):
        row_movies = trending_movies[i:i+5]
        cols = st.columns(5)
        for idx, movie in enumerate(row_movies):
            with cols[idx]:
                st.image(movie.get("poster"), width=200)
                st.subheader(movie['title'])
                st.write(f"Rating: {movie.get('avg_rating',0):.1f}")
                st.write(movie.get('stars',''))
                if movie.get('genres'):
                    badges = " ".join([f"<span class='genre-badge'>{g}</span>" for g in movie['genres'].split("|")])
                    st.markdown(badges, unsafe_allow_html=True)
                if movie.get("trailer"):
                    st.video(movie["trailer"])