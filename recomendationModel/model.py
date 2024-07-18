import movies
import pandas as pd
import requests 
import sqlite3

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

def checkMovieGenre(movie, dbTable):
    genres = [genMovie['name'] for genMovie in movie['genres']]
    for i in genres:
        for index, row in genresTable.iterrows():
            if row['genre'] == i:
                if dbTable.lower() == 'f':
                    genresTable.loc[index, 'rating'] += 10
                else:    
                    genresTable.loc[index, 'rating'] += float(cursor.execute("SELECT rating FROM wached_movies WHERE movie_id = ?", (movie['id'],)).fetchone()[0])
    return genresTable
        
        
