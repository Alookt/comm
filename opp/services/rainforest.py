import requests
from django.conf import settings

RAINFOREST_API_KEY = getattr(settings, 'RAINFOREST_API_KEY', None)
BASE_URL = "https://api.rainforestapi.com/request"

def search_amazon_products(search_term, amazon_domain="amazon.com"):
    params = {
        "api_key": RAINFOREST_API_KEY,
        "type": "search",
        "amazon_domain": amazon_domain,
        "search_term": search_term
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return None
