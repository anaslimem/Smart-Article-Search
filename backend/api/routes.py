from fastapi import APIRouter, HTTPException
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from backend.db.insert_data import index_articles
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# Get environment variables
es_url = os.getenv("ES_URL")

router = APIRouter()

# Initialize Elasticsearch client
es = Elasticsearch(es_url)

@router.get("/index_articles")
async def index_articles_route(query: str, page_size: int):
    articles = index_articles(query, page_size=page_size)
    return {"message": "Articles indexed successfully."}

@router.get("/search")
async def search_articles(query: str, page: int, page_size: int):
    """
    Search for articles in Elasticsearch with pagination.
    """
    index_name = "new_articles"
    if not query.strip():
        return {"message": "Please provide a search query."}
    
    try:
        if not es.indices.exists(index=index_name):
            return {"message": "Index does not exist. Please index some articles first."}
        
        # Calculate the starting index for pagination
        from_value = (page - 1) * page_size

        response = es.search(
            index=index_name,
            body={
                "from": from_value,
                "size": page_size,
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "content", "source"]
                    }
                }
            }
        )
        articles = [hit["_source"] for hit in response["hits"]["hits"]]
        total_results = response["hits"]["total"]["value"]

        if not articles:
            return {"message": "No articles found. Please index some articles first."}
        
        return {
            "articles": articles,
            "total_results": total_results,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_results + page_size - 1) // page_size  
        }
    except NotFoundError:
        return {"message": "Index not found. Please index some articles first."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while searching: {str(e)}")

@router.delete("/delete_index")
async def delete_index():
    """
    Delete the specified Elasticsearch index.
    """
    index_name = "new_articles"  # Default index name
    try:
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            return {"message": f"Index deleted successfully."}
        else:
            return {"message": f"No Index exists"}, 404
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete error: {str(e)}")
