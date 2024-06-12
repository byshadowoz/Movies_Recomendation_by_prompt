import requests

url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer"
}

response = requests.get(url, headers=headers)

def movies_id(res):# return all the movies in the page in a dictionary where key = id and value = title
    try:
        movies_dict = {}
        data = res.json()
        movies = data['results']
        for movie in movies:
            movies_dict[movie['id']] = movie['title']
        return movies_dict
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f'response status code: {response.status_code}')

def change_page(response, url):
    newUrl = url.split('page=')
        
    if len(newUrl) <= 1:
        return 'invalid URL'
        
    page = str(input('select num page '))
    newUrl[-1] = page
    newUrl = "page=".join(newUrl)
        
    response = requests.get(newUrl, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print('error, page does not exist')
        
    

change_page(response,url)
