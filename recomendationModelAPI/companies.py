
import requests
import os

url = "https://api.themoviedb.org/3/company/1"
api_key = os.environ['TMDB_API_KEY']

headers = {
        "accept": "application/json",
        "Authorization": "Bearer {api_key}"
}

response = requests.get(url, headers=headers)

data = response.json()

for companie in data:
    print(companie)



    

