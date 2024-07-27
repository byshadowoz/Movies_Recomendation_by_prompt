import movies
import pandas as pd
import requests 
import sqlite3
import os
import conection3 as cn3
from math import sqrt
import numpy as np
csv_path = 'allmovies.csv'
dataF = pd.read_csv(csv_path)

database = sqlite3.connect('database/usersAndMovies')
cursor = database.cursor()

url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
response = requests.get(url, headers=movies.headers)
data = response.json()

def genresForMovies():
    genresMovie = {'genres': [],
                'rating': []}
    
    for gen in data['genres']:

        genresMovie['genres'].append(gen['name'])
        genresMovie['rating'].append(int(gen['id']) * 0)

    genres = pd.DataFrame(genresMovie)
    return genres

genresTable = genresForMovies()

def movieToDf(movies):
    def genre_names(genre_list):
        return [genre['name'] for genre in genre_list]
    for movie in movies:
        movie['genres'] = genre_names(movie['genres'])

    moviesData = pd.DataFrame(movies)
    moviesData = moviesData.drop(columns=['backdrop_path', 'poster_path', 'tagline', 'homepage', 'imdb_id', 'original_language',
                                           'overview', 'production_countries', 'spoken_languages', 'status', 'production_companies','belongs_to_collection' ])
    
    print(moviesData.head())

    for index, row in dataF.iterrows():
        for genre in row['genre_ids']:
            moviesData.at[index, genre] = 1
    moviesData = moviesData.fillna(0)
    moviesData.to_csv('example.csv')
    return moviesData

allusermovies = cn3.allUserMovies('Test1', 'test1', dbTable='f')
print(movieToDf(allusermovies))

def checkMovieGenre(movie, dbTable):
    genres = [genMovie['name'] for genMovie in movie['genres']]
    for genre in genres:

        for index, row in genresTable.iterrows():
            if row['genres'] == genre:
                if dbTable.lower() == 'f':
                    genresTable.loc[index, 'rating'] += 10
                else:
                    genresTable.loc[index, 'rating'] += float(cursor.execute("SELECT rating FROM wached_movies WHERE movie_id = ?", (movie['id'],)).fetchone()[0])
    return genresTable
