from elasticsearch import Elasticsearch
from backend.api.guardian_api import fetch_guardian_articles
import os,sys

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
es = Elasticsearch("http://elasticsearch:9200")

def index_articles(query, page_size):
    """
    Fetch articles and index them into Elasticsearch.
    """
    articles = fetch_guardian_articles(query, page=1, page_size=page_size)
    index_name = "new_articles"

    for article in articles:
        doc = { 
            'title': article.get('webTitle', 'No Title'),
            'published_date': article.get('webPublicationDate', 'Unknown date'),
            'source': article.get('webUrl', 'No source URL'),
        }
        es.index(index = index_name, document=doc)
        print(f"Indexed article: {article['webTitle']}")

