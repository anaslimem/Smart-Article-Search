import streamlit as st
import requests
from datetime import datetime
from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch("http://elasticsearch:9200")

# Set the base URL of your FastAPI backend
BASE_URL = "http://backend:8000"  # Adjust if your server runs elsewhere

def index_articles(query, page_size):
    url = f"{BASE_URL}/index_articles"
    params = {"query": query, "page_size": page_size}
    response = requests.get(url, params=params)  
    print("STATUS:", response.status_code)
    print("TEXT:", response.text)
    return response.json()


def search_articles(query, page, page_size):
    url = f"{BASE_URL}/search"
    params = {"query": query, "page": page, "page_size": page_size}
    response = requests.get(url, params=params)
    return response.json()

def delete_index(index_name="new_articles"):
    url = f"{BASE_URL}/delete_index"
    params = {"index_name": index_name}
    response = requests.delete(url, params=params)
    return response.json()

def reset_search_state():
    st.session_state.search_query = ""
    st.session_state.page_size = 10
    st.session_state.page = 1
    st.session_state.search_results = None

def perform_search():
    query = st.session_state.search_query
    page_size = st.session_state.page_size
    page = st.session_state.page

    # Test case: No query provided.
    if not query.strip():
        st.session_state.search_results = {"message": "Please provide a search query."}
        return

    with st.spinner("Searching articles..."):
        result = search_articles(query, page, page_size)
        st.session_state.search_results = result

def format_published_date(date_str):
    """
    Convert a date string to YYYY/MM/DD format.
    If parsing fails, return the original string.
    """
    try:
        # Assuming the input date is in ISO format
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%Y/%m/%d")
    except Exception:
        return date_str

def main():
    st.set_page_config(page_title="Smart Article Search", layout="wide")
    st.title("Smart Article Search")
    st.write("A professional interface to index, search, and delete articles")

    # Sidebar navigation
    choice = st.sidebar.radio("Choose an option:", ["Search Articles", "Index Articles", "Delete Index"])

    if choice == "Index Articles":
        st.header("Index Articles")
        with st.form("index_form"):
            query = st.text_input("Enter search query to index articles",
                                  help="This query will be used to retrieve articles for indexing.")
            page_size = st.number_input("Enter number of articles", min_value=1, value=10, step=1)
            submit_index = st.form_submit_button("Index Articles")
            if submit_index:
                if not query.strip():
                    st.warning("Please provide a valid query to index articles.")
                else:
                    with st.spinner("Indexing articles..."):
                        result = index_articles(query, page_size)
                        st.success(result.get("message", "Articles indexed successfully."))

    elif choice == "Search Articles":
        st.header("Search Articles")
        # Initialize session state for search if not already set
        if "search_query" not in st.session_state:
            reset_search_state()

        # Search input form
        with st.form("search_form"):
            st.text_input("Search Query", key="search_query",
                          help="Search articles by keywords in title, content, or source.")
            st.number_input("Page Size", min_value=1, value=st.session_state.page_size, key="page_size", step=1)
            submitted = st.form_submit_button("Search")
            if submitted:
                st.session_state.page = 1  # Reset to first page on new search
                perform_search()

        # Display search results if available
        if st.session_state.search_results:
            result = st.session_state.search_results
            # Test case: No query provided or empty result message.
            if "message" in result:
                st.warning(result["message"])
            elif "articles" in result:
                total_results = result.get("total_results", 0)
                total_pages = result.get("total_pages", 1)
                st.write(f"**Total Results:** {total_results}")
                st.write(f"**Page {result.get('page')} of {total_pages}**")
                st.markdown("---")

                # Display each article in a neat card style
                for idx, article in enumerate(result["articles"], start=1):
                    with st.container():
                        st.subheader(f"Article {idx}")
                        for key, value in article.items():
                            # If the field is published_date, reformat it
                            if key.lower() == "published_date":
                                value = format_published_date(str(value))
                            st.write(f"**{key.capitalize()}:** {value}")
                        st.markdown("---")
                        
                # Pagination controls with unique keys and re-run to refresh the page
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("Previous", key="prev_button", disabled=st.session_state.page <= 1):
                        st.session_state.page -= 1
                        perform_search()
                        st.rerun()
                with col3:
                    if st.button("Next", key="next_button", disabled=st.session_state.page >= total_pages):
                        st.session_state.page += 1
                        perform_search()
                        st.rerun()
            else:
                st.warning("Unexpected response. Please try again.")

    elif choice == "Delete Index":
        st.header("Delete Elasticsearch Index")
        
        with st.form("delete_form"):
            index_name = "new_articles"  # Default index name
            submit_delete = st.form_submit_button("Delete Index")
            
            if submit_delete:
                with st.spinner("Checking index..."):
                    if not es.indices.exists(index=index_name):  # Check if index exists
                        st.warning(f"⚠️ Index does not exist. Nothing to delete.")
                    else:
                        result = delete_index(index_name)
                        st.success(result.get("message", f"✅ Index deleted successfully."))


if __name__ == "__main__":
    main()
