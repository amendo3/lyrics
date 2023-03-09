import requests, csv, api_key, reader
from bs4 import BeautifulSoup

client_access_token = api_key.your_client_access_token

search_term = None
artist = []

def fileOpener():
	file = open('csv.csv')
	fileReader = csv.DictReader(file, ['name'])

	for row in fileReader:
		artist.append(row['name'])

def artistPicker(list):
	for x in list:
		search_term = x
		genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"
		# print(genius_search_url)

		response = requests.get(genius_search_url)
		json_data = response.json()

		for i in range(10):
			full_title = json_data['response']['hits'][i]['result']['full_title']
			print(full_title)
			release_date = json_data['response']['hits'][i]['result']['release_date_components']
			print(release_date)
			song_path = json_data['response']['hits'][i]['result']['path']
			print(song_path)
			song_api_path = json_data['response']['hits'][i]['result']['api_path']
			print(song_api_path)



		# can add a if statement here to check if the name from the csv file actually matches the primary artist
		# listed on genius

		# can also add a check for song's lyric-state being complete or not


fileOpener()
artistPicker(artist)
