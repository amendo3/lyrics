# import modules required, as well as auxillary files with function necessary
import requests, csv, api_key, reader
from bs4 import BeautifulSoup

#set variable for api token, pull real token from .gitignored api_key file
client_access_token = api_key.your_client_access_token

# global values being used
search_term = None
artist = []


def artistPicker(list):

	for g in list:
		search_term = g
		genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"
		print(genius_search_url)



# functions being called
artistPicker(reader.artists)





# genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"

# print(genius_search_url)

# response = requests.get(genius_search_url)
# json_data = response.json()

# print(json_data['response']['hits'][0])