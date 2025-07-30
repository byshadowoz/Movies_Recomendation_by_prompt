import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

try:
    from .movie_client import MovieClient
except Exception:
    from movie_client import MovieClient


nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")


class SearchEngine:
    def __init__(self):
        self.movie_client = MovieClient()
        self.cache = {}
    
    def preprocess_text(self, prompt):

        doc = nlp(prompt.lower())
        keywords = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN", "ADJ"]]
        return list(set(keywords)) 

    def multi_search(self, keywords):
        all_results = []
        for kw in keywords:
            results = self.movie_client.get_movie_data(kw)
            all_results.extend(results)
        return all_results

    def rerank_results(self, prompt, movie_list):
        prompt_emb = model.encode(prompt, convert_to_tensor=True)
        scored = []

        for movie in movie_list:
            details = self.movie_client.get_movie_details(movie['imdbID'])
            plot = details.get('Plot')
            if not plot:
                continue
            plot_emb = model.encode(plot, convert_to_tensor=True)
            score = util.cos_sim(prompt_emb, plot_emb).item()
            scored.append((score, movie))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [movie for score, movie in scored[:10]]

if __name__ == "__main__":

    try:
        search_engine = SearchEngine()
        query = "A mind-bending thriller about dreams within dreams"
        keywords = search_engine.preprocess_text(query)
        print(f"Keywords: {keywords}")
        
        results = search_engine.multi_search(keywords)
        print(f"Found {len(results)} movies.")

        reranked = search_engine.rerank_results(query, results)
        print(f"Top reranked results: {reranked}")

    except Exception as e:
        print(f"⚠️ ERROR during execution: {e}")