import requests
import movies
import pandas as pd

url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

headers = movies.headers

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    genresGlobal = {}
    genres = data['genres']
    for genre in genres:
        genresGlobal[genre['id']] = genre['name']

def genresMovie(movies):
    pass    
