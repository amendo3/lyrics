import requests, api_key, reader, os, re, csv
from bs4 import BeautifulSoup

class artistReader():
	def __init__(self, filename):
		self.filename = filename
		self.artists = []

	def read_artists(self):
		with open(self.filename, 'r') as file:
			csv_reader = csv.reader(file)

			for row in csv_reader:
				artist_name = row[0]
				self.artists.append(artist_name)

		return self.artists

class artistIdScraper():
	def __init__(self, artists_list):
		self.artists_to_scrape = artists_list
		self.token = api_key.token
		self.ids1 = []

	def scraper(self, artists_to_scrape):
		for names in artists_to_scrape:
			id_search_term = names
			genius_search_url = f"http://api.genius.com/search?q={id_search_term}&access_token={self.token}"
			response = requests.get(genius_search_url)
			json_data = response.json()
			
			for hit in json_data['response']['hits']:
				artist_name = hit['result']['primary_artist']['name']
				if id_search_term.lower().replace(',', '') == artist_name.lower().replace(',', ''):
					primary_artist_id = hit['result']['primary_artist']['id']
					self.ids1.append(primary_artist_id)
					# primary_artist_name = hit['result']['primary_artist']['name']
					# self.artists_name_list1.append(primary_artist_name)
					break

class lyrics():
	def __init__(self):
		self.artist_reader = artistReader('artists.csv')
		self.artists = self.artist_reader.read_artists()
		self.artist_id_scraper = artistIdScraper(self.artists)
		self.artist_id_scraper.scraper(self.artists)
		self.ids = self.artist_id_scraper.ids1

	def artistFolder(self, list):
		for names in list:
			name = str(names)
			parent_dir = "/Users/amendo/repos/lyrics/files"
			path = os.path.join(parent_dir, name)

			try:
				os.mkdir(path)
			except OSError as error:
				print(error)

	

	def test(self):
		print(self.artists)
		# self.artistFolder(self.artists)
		print(self.ids)


run = lyrics()
run.test()