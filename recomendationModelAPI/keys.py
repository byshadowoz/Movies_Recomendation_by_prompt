import os

API_KEY = os.environ.get('TMDB_API_KEY') or '<YOUR TMDB API_KEY HERE>'
print(f'YOUR API KEY IS {API_KEY}')