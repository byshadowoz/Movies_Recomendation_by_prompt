
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.api.tools.search_engine import SearchEngine
from src.data.api.tools.movie_client import MovieClient
import json
import streamlit as st

def main():
    st.title("Movie Search Engine")
    
    searcher = SearchEngine()
    
    query = st.text_input("Enter your movie query:")
    
    if st.button("Search"):
        if not query:
            st.warning("Please enter a query.")
        else:
            results = searcher.intelligent_search(query)
            
            if not results:
                st.error("No results found for your query.")
            else:
                st.success(f"Found {len(results)} results:")
                for i, movie in enumerate(results, 1):
                    st.image(f"{MovieClient().get_movie_poster(movie['imdbID'])}", caption="Sunrise by the mountains")
                    st.write(f"{i}. {movie['Title']} ({movie.get('Year', '?')})")
                    st.write(f"   ⭐ Type: {movie.get('Type', 'N/A')} | 📊 Relevance: {movie['semantic_score']:.2f}")
                    
                    if i == 1:
                        details = searcher.get_movie_details(movie['imdbID'])
                        if 'Plot' in details:
                            st.write(f"   📝 Plot: {details['Plot'][:100]}...")
                        if 'Runtime' in details:
                            st.write(f"   ⏱️ Time: {details['Runtime']}")
                        if 'imdbRating' in details:
                            st.write(f"   🌟 IMDb Rating: {details['imdbRating']}")

if __name__ == "__main__":
    main()




# def main():
    
#     searcher = SearchEngine()
    
#     while True:
#         query = input("\n🔍: ")
#         if query.lower() == 'exit':
#             break
        
#         results = searcher.intelligent_search(query)
        
#         if not results:
#             print("Not found results for your query.")
#             continue
        
#         print("\n🎬 Relevant results:")
#         for i, movie in enumerate(results, 1):
#             print(f"{i}. {movie['Title']} ({movie.get('Year', '?')})")
#             print(f"   ⭐ Type: {movie.get('Type', 'N/A')} | 📊 Relevance: {movie['semantic_score']:.2f}")
            
#             if i == 1:
#                 details = searcher.get_movie_details(movie['imdbID'])
#                 if 'Plot' in details:
#                     print(f"   📝 Plot: {details['Plot'][:100]}...")
#                 if 'Runtime' in details:
#                     print(f"   ⏱️ Time: {details['Runtime']}")
#                 if 'imdbRating' in details:
#                     print(f"   🌟 IMDb Rating: {details['imdbRating']}")

# if __name__ == "__main__":
#     main()