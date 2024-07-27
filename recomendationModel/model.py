import movies
import pandas as pd
import requests 
import sqlite3
import os
import conection3 as cn3
from math import sqrt
import numpy as np
csv_path = 'allmovies.csv'
dataM = pd.read_csv(csv_path,)
dataM.drop(columns='genre_ids', inplace=True)

database = sqlite3.connect('database/usersAndMovies')
cursor = database.cursor()

url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
response = requests.get(url, headers=movies.headers)
data = response.json()

def modelRecomV1(usrnm, pswrd, dbtable):
    if dbtable.lower() == 'f':
        cursor.execute("SELECT movie_id FROM favorite_movies LEFT JOIN user ON user.id = favorite_movies.user_id WHERE name = ? AND password = ?",
                       (usrnm, pswrd))
        userMovies = cursor.fetchall()
        userData = [{'id':int(movie_id[0]), 'rating': 10} for movie_id in userMovies]
        

    elif dbtable.lower() == 'w':
        cursor.execute("SELECT movie_id, rating FROM wached_movies LEFT JOIN user ON user.id = wached_movies.user_id WHERE name = ? AND password = ?",
                       (usrnm, pswrd))
        userMovies = cursor.fetchall()
        userData = [{'id':int(movie_id[0]), 'rating': movie_id[1]} for movie_id in userMovies]
    
    inputMovie = pd.DataFrame(userData)
    Id = dataM[dataM['id'].isin(inputMovie['id'].tolist())]
    inputMovie = pd.merge(Id, inputMovie)
    inputMovie = inputMovie.drop(columns=['vote_average', 'vote_count', 'original_language','original_title'])
    inputMovie = inputMovie.reset_index(drop=True)
    genreTable = inputMovie.drop(columns=['title','adult','popularity','rating','id'])
    profile_user = genreTable.transpose().dot(inputMovie['rating'])
    genre = dataM.set_index(dataM['id'])
    genre = genre.drop(columns=['id','vote_average', 'vote_count', 'original_title','title','adult', 'popularity'])
    recom = ((genre*profile_user).sum(axis=1)) / (profile_user.sum())
    final = dataM.loc[dataM['id'].isin(recom.head(20).keys())]
    nfinal = final[['title']]
    return nfinal
print(modelRecomV1('byshadowoz', 'Togo2025$$', 'w'))