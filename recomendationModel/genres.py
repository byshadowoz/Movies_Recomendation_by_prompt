import requests
import movies

url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

headers = movies.headers

response = requests.get(url, headers=headers)

genresGlobal = {}

def genreCollection():
    if response.status_code == 200:
        data = response.json()
        genres = data['genres']
        for genre in genres:
            genresGlobal[genre['id']] = genre['name']
        return genresGlobal