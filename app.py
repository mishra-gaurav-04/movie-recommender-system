import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('movie_similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

def fetch_movies(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=3d8f4b57f82cf4a547a3892767ba501a&language=en-US',)
    data = response.json()
    return  "https://image.tmdb.org/t/p/w500/"+data['poster_path']



def recommend_movies(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x : x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_movies(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movies_posters

st.title('Movie Recommendation System')
movie_nm = st.selectbox('Choose the movies',movies['title'].values)

if st.button('Recommend Movies'):
    names,posters = recommend_movies(movie_nm)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        # st.header(names[0])
        st.image(posters[0])
    with col2:
        # st.header(names[1])
        st.image(posters[1])
    with col3:
        # st.header(names[2])
        st.image(posters[2])
    with col4:
        # st.header(names[3])
        st.image(posters[3])
    with col5:
        # st.header(names[4])
        st.image(posters[4])