
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class MovieClient:
    def __init__(self):
        self.url = 'http://www.omdbapi.com/?'
        self.api_key = os.getenv("API_K")

    def get_movie_data(self, title):
        
    
        try:
            response = requests.get(str(self.url) + f"s={title}&{self.api_key}&type=movie")
            response.raise_for_status()
            data = response.json()
            
            if data.get("Response") == "True":
                return data['Search']
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            

    def get_movie_details(self, imdb_id):
        try:
            response = requests.get(str(self.url) + f"{self.api_key}&i={imdb_id}&plot=full&type=movie")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener detalles: {e}")
            return {}
        
    def get_movie_poster(self, imdbID):

        poster = self.get_movie_details(imdbID)
        if poster:
            return poster["Poster"]
        else:
            return "https://via.placeholder.com/300x450.png?text=No+Poster+Available"
