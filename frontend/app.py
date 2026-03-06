import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
import streamlit as st
from dotenv import load_dotenv
from backend.scripts.recommender import get_recommendations
from backend.scripts.utils import load_movies_data, load_ratings_data, get_movie_poster, get_movie_trailer


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
        # Clickable button for each movie
        if st.sidebar.button(movie, key=movie):
            search_input = movie
# ------------------------
# Search bar with autocomplete
# ------------------------
search_input = st.selectbox(
    "Search movie",
    movie_titles
)

if search_input:

    # Add to history
    if search_input not in st.session_state.history:
        st.session_state.history.insert(0, search_input)
        if len(st.session_state.history) > 5:
            st.session_state.history.pop()

    # ------------------------
    # Fetch recommendations
    # ------------------------
    with st.spinner("Finding best recommendations..."):
        recommended_movies = get_recommendations(search_input)

    st.markdown("<div class='recommend-header'>Top Recommendations For You</div>", unsafe_allow_html=True)

    # Display recommended movies
    for movie in recommended_movies:
        with st.expander(f"{movie['title']} ⭐ {movie['avg_rating']:.1f}"):

            cols = st.columns([1,3])

            with cols[0]:
                poster_url = movie.get('poster_url', "https://via.placeholder.com/500x750?text=No+Image")
                st.image(poster_url, width=200)

            with cols[1]:
                st.subheader(movie['title'])
                st.write(f"Rating: {movie['avg_rating']:.1f}")
                st.write(movie['stars'])
                st.write(f"Popularity Score: {movie.get('popularity',0)}")

                if 'genres' in movie and movie['genres']:
                    genres = movie['genres'].split("|")
                    badges = " ".join([f"<span class='genre-badge'>{g}</span>" for g in genres])
                    st.markdown(badges, unsafe_allow_html=True)

                if movie.get("trailer"):
                    st.video(movie["trailer"])

# ------------------------
# TRENDING MOVIES
# ------------------------

st.markdown("---")
st.markdown("<div class='recommend-header'>🔥 Trending Movies</div>", unsafe_allow_html=True)

trending_movies = [
    "Avengers: Endgame",
    "Spider-Man: No Way Home",
    "The Dark Knight",
    "Inception",
    "Interstellar"
]

for title in trending_movies:

    poster = get_movie_poster(title, TMDB_API_KEY)
    trailer = get_movie_trailer(title, TMDB_API_KEY)

    with st.expander(title):

        cols = st.columns([1,3])

        with cols[0]:
            st.image(poster, width=200)

        with cols[1]:
            st.subheader(title)

            if trailer:
                st.video(trailer)