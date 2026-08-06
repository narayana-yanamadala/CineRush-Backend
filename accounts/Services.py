import requests
from django.conf import settings

def search_movie(title):
    url = "https://www.omdbapi.com/"

    params = {
        "apikey": settings.OMDB_API_KEY,
        "t": title
    }

    response = requests.get(url, params=params)
    return response.json()