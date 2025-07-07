# 📚 Book Recommender AI Model App

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Keras](https://img.shields.io/badge/Keras-Autoencoder-orange?logo=keras)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 🚀 AI-Powered Personalized Book Recommendation System

An intelligent book recommender web app powered by **Keras Autoencoders** and **Streamlit**, designed to suggest personalized book titles based on collaborative filtering. This project combines deep learning with a sleek UI and interactive filter-based search experience.

---

## ✨ Key Features

- 🔍 **Collaborative Filtering**: Personalized recommendations by analyzing user behavior
- 🌐 **Filter-Based Discovery**:
  - Filter by **Genre**, **Author**, or **Minimum Rating**
  - Combine filters for refined results
- 🎨 **Modern UI**:
  - Streamlit dark theme with gradient buttons, hover effects, shadows
  - **Lottie animation** intro splash screen
  - Responsive layout and styled DataFrames
- 📤 **CSV Export**: Download your recommendations for later use

---

## 🧠 Built With

- **Frontend/UI**: Streamlit, HTML/CSS (via Markdown), Lottie
- **ML Model**: Keras Autoencoder
- **Data Handling**: Pandas, NumPy
- **Assets**:
  - `book_predictions.npy`: Autoencoder prediction matrix
  - `ratings_train.npy`: Training interaction matrix
  - `merged_data.csv`: Cleaned dataset of books, users, ratings
  - `Animation - 1751816715171.json`: Lottie animation for intro

---

## 🛠️ How It Works

- Encodes the user-book interaction matrix using an autoencoder
- Predicts missing ratings by reconstructing the full matrix
- Masks already rated books from recommendations
- Combines collaborative and filter-based approaches
- Loads large numpy files with `mmap_mode='r'` to reduce RAM usage
- Utilizes `@st.cache_resource` for faster Streamlit re-runs

---

## 📦 Project Structure

```
📦 Book-Recommender-AI-Model-App
├── 📜 BOOK_REC_APP.py                # Streamlit app frontend
├── 📓 ML.ipynb                       # Jupyter notebook for model training
├── 📄 LICENSE
├── 📄 README.md
├── 📦 RAW SOURCED DATABASE FILES.zip # Zipped raw datasets
├── 📄 book_autoencoder_epoch12.h5    # Trained Keras autoencoder model
├── 📄 Animation - 1751816715171.json # Lottie animation file
```

---

## 🚀 Run the App Locally

```bash
# Clone this repo
$ git clone https://github.com/Pranitttt64/Book-Recommender-AI-Model-App.git
$ cd Book-Recommender-AI-Model-App

# (Optional but recommended) Create virtual environment
$ python -m venv venv
$ venv\Scripts\activate     # On Windows

# Install dependencies
$ pip install -r requirements.txt

# Run the app
$ streamlit run BOOK_REC_APP.py
```

---

## 🙋‍♂️ Author

Built with ❤️ by **Pranit Saundankar**

- [LinkedIn]([https://www.linkedin.com/in/pranitsaundankar](https://www.linkedin.com/in/pranit-saundankar-68532328b/))
- [GitHub](https://github.com/Pranitttt64)

---

## 🏷️ Tags

`Deep Learning` `Recommender System` `Streamlit` `Keras` `Python` `Portfolio Project` `Autoencoder`

---
