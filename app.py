from flask import Flask, render_template, request, redirect, url_for, flash
import os, requests

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "mysecret123")

OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "1225e9aa")

def fetch_movie(title):
    """Fetch movie details by title from OMDb."""
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

@app.template_filter("get_poster_url")
def get_poster_url_filter(poster):
    """Return valid poster URL or fallback image."""
    return poster if poster and poster != "N/A" else "https://via.placeholder.com/300x445?text=No+Image"

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    content_results = []
    content_type = "all"
    error_message = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        content_type = request.form.get("content_type", "all")
        if not query:
            error_message = "Please enter a title to search."
        else:
            url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}&type={content_type if content_type!='all' else ''}"
            r = requests.get(url)
            data = r.json()
            if data.get("Response") == "True":
                content_results = data.get("Search", [])
            else:
                error_message = data.get("Error", "No results found.")
    else:
        # Default: show trending/popular movies
        trending_titles = ["Oppenheimer", "Barbie", "Dune", "The Dark Knight", "Stranger Things"]
        for title in trending_titles:
            movie = fetch_movie(title)
            if movie and movie.get("Response") == "True":
                movie["content_type"] = "movie"
                content_results.append(movie)

    return render_template("index.html",
                           content_results=content_results,
                           query=query,
                           content_type=content_type,
                           error_message=error_message)

@app.route("/details/<imdb_id>")
def content_details(imdb_id):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}&plot=full"
    r = requests.get(url)
    data = r.json() if r.status_code == 200 else {}
    return render_template("details.html", content=data)
