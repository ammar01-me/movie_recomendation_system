import pandas as pd
import streamlit as st
import pickle
import requests
df = pd.read_csv('web_app\movies_data.csv')
similarity = pickle.load(open('web_app\\similarity_arr.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def info(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    d1 = data['overview']
    d2 = data['popularity']
    d3 = data['release_date']
    d4 = data['status']
    data_dict = {'overview':d1,'popularity':d2,'release_date':d3,'status':d4}
    return data_dict

def recommend_movie(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_lst = sorted(list(enumerate(distances)),reverse=True,key=(lambda x: x[1]))
    five_movie = movie_lst[:6]

    lst_of_movies = []
    lst_of_poster_path = []
    lst_of_info = []
    for i in five_movie:
        lst_of_movies.append(df.iloc[i[0]]['title'])

    for i in five_movie:
        url = fetch_poster(df.iloc[i[0]]['id'])
        lst_of_poster_path.append(url)
    
    for i  in five_movie:
        lst_of_info.append(info(df.iloc[i[0]]['id']))
    return lst_of_movies,lst_of_poster_path,lst_of_info

st.title('Movie Recomendation System🎬')
st.caption('the data is collected form imdb site')

movie_name = st.selectbox('Chose a movie that you liked',df['title'])
rec = st.button('Recommend')
if rec:
    try:
        lst_of_movies,lst_of_poster_path,lst_of_info = recommend_movie(movie_name)
        col1,col2,col3,col4,col5  = st.columns(5)
        col_lst = [col1,col2,col3,col4,col5]
        for i in range(5):
            with col_lst[i]:
                st.write(lst_of_movies[i])
                st.image(lst_of_poster_path[i])
                st.write(':green[overview]')
                st.caption(lst_of_info[i]['overview'])
                st.write(':green[popularity]')
                st.caption(f'⭐{lst_of_info[i]['popularity']}')
                st.write(':green[release_date]')
                st.caption(lst_of_info[i]['release_date'])
                st.write(':green[status]')
                st.caption(lst_of_info[i]['status'])

    except Exception as e:
        st.write('An error occured..')
        st.caption(e)
        