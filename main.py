import requests, api_key
from bs4 import BeautifulSoup

client_access_token = api_key.your_client_access_token

search_term = "Missy Elliott"
genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"

#print(genius_search_url)

response = requests.get(genius_search_url)
json_data = response.json()

print(json_data['response']['hits'][0])