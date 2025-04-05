import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

def fetch_guardian_articles(query, page, page_size)-> dict:
    """
    Fetch articles from The Guardian API based on the provided query and page number.

    Args:
        query (str): The search query.
        page (int): The page number for pagination.

    Returns:
        dict: A dictionary containing the response from The Guardian API.
    """
    params = {
        'q': query,
        'page': page,
        'api-key': API_KEY,
        'page-size': page_size
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        articles = data['response']['results']
        return articles
    else:
        return {"error": "Failed to fetch articles"}
