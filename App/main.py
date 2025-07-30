
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.api.tools.search_engine import SearchEngine
from src.data.api.tools.movie_client import MovieClient
import json
import streamlit as st

def movie_front(results):
    for movie in results:
        i = 1
        if 'Poster' in movie:
            st.image(f"{MovieClient().get_movie_poster(movie['imdbID'])}")
                        
        st.write(f"{i}. {movie['Title']} ({movie.get('Year', '?')})")
        st.write(f"   ⭐ Type: {movie.get('Type', 'N/A')}")
                         
        if i:
            details = MovieClient().get_movie_details(movie['imdbID'])
            if 'Plot' in details:
                st.info(f"   📝 Plot: {details['Plot']}")

            if 'Runtime' in details:
                st.write(f"   ⏱️ Time: {details['Runtime']}")

            if 'imdbRating' in details:
                st.write(f"   🌟 IMDb Rating: {details['imdbRating']}")
        i+= 1

def main():
    st.title("Movie Search Engine")
    
    searcher = SearchEngine()
    
    query = st.text_input("Enter your movie query:")

    if query:
        keywords = searcher.preprocess_text(query)

        results = searcher.multi_search(keywords)

        top_movies = searcher.rerank_results(query, results)

        if top_movies:
            movie_front(top_movies)
            
        else:
            st.error('No movies Found')

    
                

if __name__ == "__main__":
    try:

        main()
        
    except Exception:
        st.error('Something is Wrong...')