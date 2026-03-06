# 🎬 Hybrid Movie Recommender System

GitHub Repository: [Hybrid Movie Recommender](https://github.com/Lucy-Bentum/Hybrid-Movie-Recommender.git)

---

## 📌 Project Overview

The **Hybrid Movie Recommender System** is an AI-powered web application that provides movie recommendations based on user search input. The system combines multiple recommendation techniques to generate accurate and personalized suggestions.

It integrates **content-based filtering**, **collaborative filtering signals**, and **popularity-based scoring**, along with the **TMDB API** to fetch movie posters and trailers for an interactive user experience.

---

## 🚀 Features

- Movie search with autocomplete
- Hybrid recommendation system (content + collaborative)
- Movie posters and trailers via TMDB API
- Star ratings and popularity scores
- Recently searched movie history
- Trending movies section
- Clean and responsive UI built with Streamlit

---

## 🧠 AI Approach

This system uses a **Hybrid Recommendation Model** combining:

### 1️⃣ Content-Based Filtering

Recommends movies with similar metadata such as genres.

### 2️⃣ Collaborative Filtering Signals

Analyzes user rating patterns to suggest popular or related movies.

### 3️⃣ Popularity Scoring

A hybrid score is calculated as:
Score = (Average Rating × 0.7) + (Popularity × 0.3)
This balances **quality** and **popularity** for better recommendations.

---

## 🧩 Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- FuzzyWuzzy (fuzzy search)
- TMDB API
- HTML/CSS for styling

---

## 📂 Project Structure

HybridMovieRecommender/
├── backend/
│ └── scripts/
│ ├── recommender.py
│ ├── hybrid_model.py
│ └── utils.py
├── frontend/
│ ├── app.py
│ └── assets/
│ └── styles.css
├── data/
│ ├── movies.csv
│ ├── ratings.csv
│ └── tags.csv
├── .env
├── .gitignore
├── requirements.txt
└── README.md

## 🔑 API Configuration

The project uses **TMDB API** for posters and trailers.  

Create a `.env` file in the root directory:
TMDB_API_KEY=your_api_key_here
**Note:** `.env` is included in `.gitignore` to keep your API key private.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Lucy-Bentum/Hybrid-Movie-Recommender.git
Navigate to the project folder:

cd Hybrid-Movie-Recommender
Install dependencies:

pip install -r requirements.txt
Run the Streamlit application:

streamlit run frontend/app.py
📊 Dataset
This project uses the MovieLens dataset, containing:

Movie metadata

User ratings

Movie tags

Dataset Source: MovieLens 100k Dataset

🔮 Future Improvements
User login system

Watch-history-based recommendations

Deep learning recommendation models

Real-time trending movie API

Personalized recommendation profiles

👨‍💻 Author
Developed as part of an AI recommendation system project.

📜 License
MIT License – for educational and research purposes.


---

This README is **ready to go**:

- ✅ Proper headers, links, and markdown formatting  
- ✅ Uses your GitHub URL correctly  
- ✅ No underlines or broken links  
- ✅ Safe reference to `.env`  

---

Next step:  

1. **Place this README.md** in the root of your project folder.  
2. Open terminal in your project folder and run:

```bash
git add README.md
git commit -m "Add full README"
git push.
