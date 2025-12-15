import streamlit as st
import pickle
import pandas as pd
import requests

# ------------------ FETCH POSTER ------------------
def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey=166ae9c8"
    response = requests.get(url)
    data = response.json()

    if data.get("Poster") != "N/A":
        return data["Poster"]
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# ------------------ RECOMMEND ------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    reco_movies = []
    reco_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        reco_movies.append(title)
        reco_posters.append(fetch_poster(title))

    return reco_movies, reco_posters

# ------------------ LOAD DATA ------------------
movies_dict = pickle.load(open('netflix/movies_dct.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('netflix/similarity.pkl', 'rb'))

# ------------------ UI ------------------
st.title(" 🎬 Movie Recommendation System ")

option = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(option)
    st.markdown(
"""
<style>
.movie-poster img {
    border-radius: 14px;
    height: 320px;
    width: 100%;
    object-fit: cover;
    box-shadow: 0 6px 15px rgba(0,0,0,0.35);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}
.movie-poster img:hover {
    transform: scale(1.08);
    box-shadow: 0 12px 25px rgba(0,0,0,0.5);
}
.movie-title {
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    margin-top: 8px;
    color: #333;
    transition: color 0.3s ease;
}
.movie-title:hover {
    color: #ff4b2b;
}
</style>
""",
unsafe_allow_html=True
)



    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{poster}" width="100%">
                    <div class="movie-title">{name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
