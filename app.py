import os
import gdown
import streamlit as st
import pickle
import pandas as pd
import requests

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ================= CSS =================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0f0f0f;
}

/* Title */
.title {
    text-align: center;
    font-size: 34px;
    font-weight: 600;
    color: white;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #bbb;
    margin-bottom: 25px;
}

/* Movie card */
.movie-card {
    text-align: center;
}

/* Poster */
.movie-card img {
    height: 250px;
    border-radius: 10px;
    transition: 0.3s;
}

/* Hover */
.movie-card img:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px rgba(0,140,255,0.7);
}

/* Movie title */
.movie-title {
    margin-top: 10px;
    font-size: 15px;
    color: white;
    font-weight: bold;
}

/* Button */
.stButton>button {
    background-color: #e50914;
    color: white;
    border-radius: 6px;
    height: 40px;
    width: 150px;
}

/* Dropdown */
.stSelectbox div {
    background-color: #222 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# ================= FETCH POSTER =================
def fetch_poster(movie_id):
    api_key = st.secrets["api_key"]   # <-- secure key

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    response = requests.get(url)
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



# ================= RECOMMEND =================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# ================= LOAD DATA =================
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Download similarity.pkl if not present
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=1LI6eczGb0BJ894hlT4uauZpdSxZU4Hgq"
    gdown.download(url, "similarity.pkl", quiet=False)

similarity = pickle.load(open('similarity.pkl', 'rb'))


# ================= CENTER LAYOUT =================
left, center, right = st.columns([1, 2, 1])

with center:

    st.markdown('<div class="title">🎬 Movie Recommender</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Discover movies like Netflix</div>', unsafe_allow_html=True)

    selected_movie = st.selectbox(
        "Choose a movie",
        movies['title'].values
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Recommend"):
        names, posters = recommend(selected_movie)

        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.markdown(f"""
                    <div class="movie-card">
                        <img src="{posters[i]}">
                        <div class="movie-title">{names[i]}</div>
                    </div>
                """, unsafe_allow_html=True)
