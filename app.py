from flask import Flask, render_template, request, url_for
import os, requests

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "mysecret123")

OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "1225e9aa")

def fetch_movies(query, content_type="all", page=1):
    """Fetch movies/series list from OMDb with pagination."""
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}&page={page}"
    if content_type != "all":
        url += f"&type={content_type}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else {}

def fetch_movie(title):
    """Fetch movie by title."""
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else {}

@app.template_filter("get_poster_url")
def get_poster_url_filter(poster):
    return poster if poster and poster != "N/A" else "https://via.placeholder.com/300x445?text=No+Image"

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.args.get("query", "").strip()
    genre = request.args.get("genre", "")
    page = int(request.args.get("page", 1))
    content_results = []
    error_message = ""

    if genre:
        # Show movies by genre (fake, since OMDb doesn’t allow genre search directly → we simulate with keywords)
        query = genre

    if query:
        data = fetch_movies(query, page=page)
        if data.get("Response") == "True":
            content_results = data.get("Search", [])
        else:
            error_message = data.get("Error", "No results found.")
    else:
        # Default trending movies
        trending_titles = ["Oppenheimer", "Barbie", "Dune", "The Dark Knight",
                           "Stranger Things", "Avengers", "Titanic", "Naruto",
                           "Interstellar", "Frozen", "Joker", "John Wick",
                           "The Matrix", "Iron Man", "Shrek", "Spider-Man"]
        for title in trending_titles:
            movie = fetch_movie(title)
            if movie and movie.get("Response") == "True":
                content_results.append(movie)

    return render_template("index.html",
                           content_results=content_results,
                           query=query,
                           genre=genre,
                           page=page,
                           error_message=error_message)

@app.route("/details/<imdb_id>")
def content_details(imdb_id):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}&plot=full"
    r = requests.get(url)
    data = r.json() if r.status_code == 200 else {}
    return render_template("details.html", content=data)
