import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model
from streamlit_lottie import st_lottie
import json
import os
import base64

# Configure page
st.set_page_config(page_title="📚 Book Recommender", layout="wide")

# ---------- Custom CSS Styling ----------
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #0e1117;
        color: #FAFAFA;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1f6feb, #2ea44f);
        color: white;
        padding: 0.6em 1.2em;
        border: none;
        border-radius: 10px;
        font-size: 1em;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #2ea44f, #1f6feb);
    }
    .stDownloadButton>button {
        border-radius: 8px;
        background: #2ea44f;
        color: white;
        transition: 0.3s ease;
    }
    .stDownloadButton>button:hover {
        background: #238636;
        transform: scale(1.03);
    }
    .stSelectbox>div>div>div {
        background-color: #161b22 !important;
        color: white !important;
    }
    .stSlider>div>div>div>div {
        background: #238636 !important;
    }
    .stDataFrame {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Load Animation JSON ----------
def load_lottie(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# Load animation from file
lottie_animation = load_lottie("D:\PranitCode\Projects\Book-Recommender-AI-Model-App\Animation - 1751816715171.json")

# ---------- Load Data Efficiently ----------
@st.cache_resource(show_spinner=False)
def load_data():
    usecols = ['user_id', 'book_id', 'title', 'genre', 'authors', 'average_rating']
    df = pd.read_csv("merged_data.csv", usecols=usecols)
    df['user_index'] = df['user_id'].astype('category').cat.codes
    df['book_index'] = df['book_id'].astype('category').cat.codes
    book_lookup = df[['book_index', 'title']].drop_duplicates().set_index('book_index')

    predicted_ratings = np.load("book_predictions.npy", mmap_mode='r')
    ratings_train = np.load("ratings_train.npy", mmap_mode='r')
    return df, predicted_ratings, ratings_train, book_lookup

def recommend_books(user_id, predicted_ratings, ratings_train, df, book_lookup, top_n=5):
    try:
        user_index = df[df['user_id'] == user_id]['user_index'].iloc[0]
    except IndexError:
        return pd.DataFrame([{"title": "❌ Invalid user ID"}])
    preds = predicted_ratings[user_index].copy()
    rated_books = ratings_train[user_index].nonzero()[0]
    preds[rated_books] = -np.inf
    top_indices = preds.argsort()[-top_n:][::-1]
    return book_lookup.loc[top_indices].reset_index(drop=True)

def recommend_by_filters(df, genre=None, author=None, min_rating=None, top_n=5):
    filtered = df.copy()
    if genre:
        filtered = filtered[filtered['genre'] == genre]
    if author:
        filtered = filtered[filtered['authors'] == author]
    if min_rating is not None:
        filtered = filtered[filtered['average_rating'] >= min_rating]
    return filtered[['title', 'authors', 'average_rating']].drop_duplicates(subset=['title'])\
        .sort_values(by='average_rating', ascending=False).head(top_n)

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ---------- Load Data ----------
with st.spinner("Loading data..."):
    df, predicted_ratings, ratings_train, book_lookup = load_data()

# ---------- Header + Animation ----------
if lottie_animation:
    st_lottie(lottie_animation, speed=1.2, height=250, key="bookload")
else:
    st.warning("📁 Lottie animation file not found. Skipping animation...")

st.title("📖 Welcome to the Personalized Book Recommender 👋")
st.caption("✨ Discover top books tailored to your taste with AI magic")

# ---------- Sidebar Filters ----------
with st.sidebar:
    st.header("🔍 Recommendation Options")
    rec_type = st.radio("Choose Recommendation Type:", [
        "Collaborative Filtering (User ID)",
        "Filter by Genre",
        "Filter by Author",
        "Filter by Rating",
        "Combine Filters"
    ])

st.markdown("---")

# ---------- Main Logic ----------
if rec_type == "Collaborative Filtering (User ID)":
    st.subheader("🔑 User-Based Recommendations")
    user_ids = sorted(df['user_id'].unique())
    user_id = st.selectbox("Select User ID", options=user_ids)
    top_n = st.slider("Number of Recommendations", 1, 10, 5)
    if st.button("Get Recommendations"):
        recommendations = recommend_books(user_id, predicted_ratings, ratings_train, df, book_lookup, top_n)
        st.dataframe(recommendations, use_container_width=True)
        st.download_button("📥 Download CSV", convert_df_to_csv(recommendations), "recommendations.csv", "text/csv")

elif rec_type == "Filter by Genre":
    st.subheader("🌈 Genre-Based Recommendations")
    genre_options = sorted(df['genre'].dropna().unique())
    genre = st.selectbox("Choose Genre", options=genre_options)
    top_n = st.slider("Top N Books", 1, 10, 5)
    results = recommend_by_filters(df, genre=genre, top_n=top_n)
    st.dataframe(results, use_container_width=True)
    st.download_button("📥 Download CSV", convert_df_to_csv(results), "genre_recommendations.csv", "text/csv")

elif rec_type == "Filter by Author":
    st.subheader("👨‍🏫 Author-Based Recommendations")
    author_options = sorted(df['authors'].dropna().unique())
    author = st.selectbox("Choose Author", options=author_options)
    top_n = st.slider("Top N Books", 1, 10, 5)
    results = recommend_by_filters(df, author=author, top_n=top_n)
    st.dataframe(results, use_container_width=True)
    st.download_button("📥 Download CSV", convert_df_to_csv(results), "author_recommendations.csv", "text/csv")

elif rec_type == "Filter by Rating":
    st.subheader("⭐ Top Rated Books")
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 4.0, step=0.1)
    top_n = st.slider("Top N Books", 1, 10, 5)
    results = recommend_by_filters(df, min_rating=min_rating, top_n=top_n)
    st.dataframe(results, use_container_width=True)
    st.download_button("📥 Download CSV", convert_df_to_csv(results), "rating_recommendations.csv", "text/csv")

elif rec_type == "Combine Filters":
    st.subheader("🌐 Advanced Search")
    genre_options = sorted(df['genre'].dropna().unique())
    author_options = sorted(df['authors'].dropna().unique())
    genre = st.selectbox("Choose Genre (optional)", options=["None"] + genre_options)
    author = st.selectbox("Choose Author (optional)", options=["None"] + author_options)
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 4.0, step=0.1)
    top_n = st.slider("Top N Books", 1, 10, 5)
    genre_val = genre if genre != "None" else None
    author_val = author if author != "None" else None
    results = recommend_by_filters(df, genre=genre_val, author=author_val, min_rating=min_rating, top_n=top_n)
    st.dataframe(results, use_container_width=True)
    st.download_button("📥 Download CSV", convert_df_to_csv(results), "combined_recommendations.csv", "text/csv")

st.markdown("---")
st.caption("📘 Built by Pranit — using Streamlit + Keras Autoencoder")
