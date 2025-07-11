import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .movie_client import MovieClient


nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):

    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def semmantic_search(query, documents):


    processed_docs = [preprocess_text(doc) for doc in documents]
    processed_query = preprocess_text(query)

    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(processed_docs)
    query_vector = vectorizer.transform([processed_query])

    similarities = cosine_similarity(query_vector, doc_vectors).flatten()
    return similarities

class SearchEngine:
    def __init__(self):
        self.movie_client = MovieClient()
        self.cache = {}
    
    def intelligent_search(self, query, top_n=5):

        raw_results = self.movie_client.get_movie_data(query)

        if not raw_results:
            return []
        
        movie_texts = [
            f"{movie.get('Title')} {movie.get('Year', '')} {movie.get('Type', '')}"
            for movie in raw_results
        ]

        similarities = semmantic_search(query, movie_texts)

        scored_movies = []
        for idx, movie in enumerate(raw_results):
            movie["semantic_score"] = similarities[idx]
            scored_movies.append(movie)

        sorted_movies = sorted(
            scored_movies,
            key=lambda x: x["semantic_score"],
            reverse=True
        )
        
        return sorted_movies[:top_n]
    
    def get_movie_details(self, imdb_id):
        if imdb_id not in self.cache:
            self.cache[imdb_id] = self.movie_client.get_movie_details(imdb_id)
        return self.cache[imdb_id]
    

if __name__ == "__main__":
    search_engine = SearchEngine()
    query = "A mind-bending thriller about dreams within dreams"
    results = search_engine.intelligent_search(query)
    
    for movie in results:
        print(f"Title: {movie['title']}, Score: {movie['semantic_score']}")
        print(f"Plot: {movie.get('Plot', 'No plot available')}\n")