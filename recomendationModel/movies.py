import requests
import dotenv
import os 

dotenv.load_dotenv()

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.environ.get('api_rat') or '<YOUR ACCESS TOKEN>'}"
}

def movies_id():# return all the movies in the page in a dictionary where key = id and value = title
    try:
        response = change_page()
        movies_dict = {}
        data = response.json()
        movies = data['results']
        for movie in movies:
            movies_dict[movie['id']] = movie
        return movies_dict
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f'response status code: {response.status_code}')

def change_page():
    num = int(input('select page => '))
    if num < 1:
        num = 1
    print(f'fetching page {num}')
    return requests.get(f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={num}", headers=headers)

def main_test():
    try:
        movies_dict = movies_id()
        print(movies_dict)
    except Exception as e:
        print('error, could not fetch data')