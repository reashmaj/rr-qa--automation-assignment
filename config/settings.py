BASE_URL = "https://tmdb-discover.surge.sh/"
API_BASE_URL = "https://api.themoviedb.org/3"

CATEGORIES = ["Popular", "Trending", "Newest", "Top Rated"]
CONTENT_TYPES = ["Movies", "TV Shows"]

GENRES_MOVIES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime",
    "Documentary", "Drama", "Family", "Fantasy", "History",
    "Horror", "Music", "Mystery", "Romance", "Science Fiction",
    "TV Movie", "Thriller", "War", "Western"
]

GENRES_TV = [
    "Action & Adventure", "Animation", "Comedy", "Crime",
    "Documentary", "Drama", "Family", "Kids", "Mystery",
    "News", "Reality", "Sci-Fi & Fantasy", "Soap",
    "Talk", "War & Politics", "Western"
]

TIMEOUTS = {
    "page_load": 30000,
    "element_visible": 10000,
    "api_response": 15000,
    "animation": 1000,
}
