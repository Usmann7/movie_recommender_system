import streamlit as st
import pickle
import requests

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ------------------ LOAD DATA ------------------
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# ------------------ TMDB API ------------------
API_KEY = "2264d7216f01f001887373153d0565b4"


# ------------------ FETCH POSTER ------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path

    return None


# ------------------ RECOMMEND MOVIES ------------------
def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]]["movie_id"]

        recommended_movies.append(
            movies.iloc[i[0]]["title"]
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters


# ------------------ UI ------------------

st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a Movie",
    movies["title"].values,
    key="movie_select"
)

if st.button("Recommend"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            st.write(names[i])

            if posters[i]:
                st.image(posters[i], use_container_width=True)
            else:
                st.write("Poster not available")