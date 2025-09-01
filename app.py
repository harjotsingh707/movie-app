import os
import logging
from flask import Flask, render_template, request, flash
import requests

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# OMDB API Configuration
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "your_omdb_api_key_here")
OMDB_BASE_URL = "http://www.omdbapi.com"

def search_content_omdb(query, content_type="all"):
    """Search for movies, series, or both using OMDB API"""
    try:
        all_results = []
        
        # Search types based on user selection
        search_types = []
        if content_type in ["all", "movie"]:
            search_types.append("movie")
        if content_type in ["all", "series"]:
            search_types.append("series")
        
        for search_type in search_types:
            url = OMDB_BASE_URL
            params = {
                "apikey": OMDB_API_KEY,
                "s": query,
                "type": search_type
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("Response") == "True":
                results = data.get("Search", [])
                # Add content type for easier filtering in templates
                for result in results:
                    result['content_type'] = search_type
                all_results.extend(results)
        
        return all_results
        
    except Exception as e:
        logging.error(f"Failed to search content: {e}")
        return []

def get_content_details_omdb(imdb_id):
    """Get detailed information for movies or series using OMDB API"""
    try:
        url = OMDB_BASE_URL
        params = {
            "apikey": OMDB_API_KEY,
            "i": imdb_id,
            "plot": "full"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "True":
            return data
        else:
            logging.warning(f"OMDB details failed: {data.get('Error', 'Unknown error')}")
            return None
    except Exception as e:
        logging.error(f"Failed to get content details: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    """Home page with content search functionality (movies, series, anime)"""
    content_results = []
    query = ""
    content_type = "all"
    error_message = ""
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        content_type = request.form.get("content_type", "all")
        
        if not query:
            error_message = "Please enter a title to search."
        else:
            try:
                # Search for content using OMDB
                content_results = search_content_omdb(query, content_type)
                
                if not content_results:
                    content_name = {
                        "movie": "movies",
                        "series": "series", 
                        "all": "movies or series"
                    }.get(content_type, "content")
                    error_message = f"No {content_name} found for '{query}'. Try a different search term."
                    
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                error_message = "An unexpected error occurred. Please try again."
    
    return render_template("index.html", 
                         content_results=content_results, 
                         query=query, 
                         content_type=content_type,
                         error_message=error_message)

@app.route("/details/<imdb_id>")
def content_details(imdb_id):
    """Content details page for movies and series using OMDB"""
    try:
        # Get content details using OMDB
        content = get_content_details_omdb(imdb_id)
        
        if not content:
            flash("Content not found.", "error")
            return render_template("details.html", content=None)
            
        return render_template("details.html", content=content)
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again.", "error")
        return render_template("details.html", content=None)

# TV shows route removed - OMDB focuses on movies

@app.template_filter('get_poster_url')
def get_poster_url(poster_url):
    """Get poster URL or return placeholder for OMDB"""
    if poster_url and poster_url != "N/A":
        return poster_url
    return "https://via.placeholder.com/500x750/1a1a1a/ffffff?text=No+Image"

@app.template_filter('format_omdb_rating')
def format_omdb_rating(imdb_rating):
    """Format OMDB rating for display"""
    if imdb_rating and imdb_rating != "N/A":
        return f"{imdb_rating}/10"
    return "N/A"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
