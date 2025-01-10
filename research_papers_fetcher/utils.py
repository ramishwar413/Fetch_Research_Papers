import requests
from typing import Dict

def make_request(url: str, params: Dict) -> Dict:
    """Makes a GET request to a specified URL with parameters."""
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
