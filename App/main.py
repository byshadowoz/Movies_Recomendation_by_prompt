
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.api.tools.search_engine import SearchEngine
from src.data.api.tools.movie_client import MovieClient
import json

def main():
    
    searcher = SearchEngine()
    
    while True:
        query = input("\n🔍: ")
        if query.lower() == 'exit':
            break
        
        results = searcher.intelligent_search(query)
        
        if not results:
            print("Not found results for your query.")
            continue
        
        print("\n🎬 Relevant results:")
        for i, movie in enumerate(results, 1):
            print(f"{i}. {movie['Title']} ({movie.get('Year', '?')})")
            print(f"   ⭐ Type: {movie.get('Type', 'N/A')} | 📊 Relevance: {movie['semantic_score']:.2f}")
            
            if i == 1:
                details = searcher.get_movie_details(movie['imdbID'])
                if 'Plot' in details:
                    print(f"   📝 Plot: {details['Plot'][:100]}...")
                if 'Runtime' in details:
                    print(f"   ⏱️ Time: {details['Runtime']}")
                if 'imdbRating' in details:
                    print(f"   🌟 IMDb Rating: {details['imdbRating']}")

if __name__ == "__main__":
    main()