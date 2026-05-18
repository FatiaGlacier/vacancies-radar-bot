from ..config import get_rapidapi_token
import requests
import json

BASE_URL = "https://jsearch.p.rapidapi.com/search-v2"

headers = {
	f"x-rapidapi-key": get_rapidapi_token,
	"x-rapidapi-host": "jsearch.p.rapidapi.com",
	"Content-Type": "application/json"
}