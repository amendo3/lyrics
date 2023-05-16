import requests, api_key, reader, os, re, csv
from bs4 import BeautifulSoup

class Artist():
	def __init__(self, name, ids=None):
		self.name = name
		self.ids = ids

class Album():
	def __init__(self, artist, name = None, ids=None, date=None):
		self.artist = artist
		self.name = name
		self.ids = ids
		self.date = date

class artistReader():
	def __init__(self, filename):
		self.filename = filename
		self.artists = []

	def read_artists(self):
		with open(self.filename, 'r') as file:
			csv_reader = csv.reader(file)

			for row in csv_reader:
				artist_name = row[0]
				artist = Artist(artist_name)
				self.artists.append(artist)

		return self.artists

class artistIdScraper():
	def __init__(self, artists_list):
		self.artists_to_scrape = artists_list
		self.token = api_key.token

	def scraper(self):
		for artist in self.artists_to_scrape:
			id_search_term = artist.name
			genius_search_url = f"http://api.genius.com/search?q={id_search_term}&access_token={self.token}"
			response = requests.get(genius_search_url)
			json_data = response.json()
			
			for hit in json_data['response']['hits']:
				artist_name = hit['result']['primary_artist']['name']
				if id_search_term.lower().replace(',', '') == artist_name.lower().replace(',', ''):
					primary_artist_id = hit['result']['primary_artist']['id']

					artist.ids = primary_artist_id
					break

class lyrics():
	def __init__(self):
		self.artist_reader = artistReader('artists.csv')
		self.artists = self.artist_reader.read_artists()
		self.artist_id_scraper = artistIdScraper(self.artists)


		self.albums = []

	def artistFolder(self, list):
		for names in list:
			name = str(names)
			parent_dir = "/Users/amendo/repos/lyrics/files"
			path = os.path.join(parent_dir, name)

			try:
				os.mkdir(path)
			except OSError as error:
				print(error)


	def get_artist_ids(self):
		self.artist_id_scraper.scraper()

	def album_list(self):
		for artist in self.artists:
			artist_id_term = artist.ids
			public_url_albums = f"http://genius.com/api/artists/{artist_id_term}/albums?per_page=50/"

			response = requests.get(public_url_albums)
			album_json_data = response.json()

			for albums in album_json_data['response']['albums']:
				if albums['_type'] == "album":
					album_id = albums['api_path']
					album_name = albums['name']
					album_date = albums['release_date_for_display']

					album = Album(artist, album_name, album_id, album_date)
					self.albums.append(album)


				else:
					print('ALBUM LIST ERROR')
					break


	def test(self):
		print([artist.name for artist in self.artists])
		print([artist.ids for artist in self.artists])

		for album in self.albums:
			print(album.ids)

		for artist in self.artists:
			artist_name = artist.name
			artist_albums = [album for album in self.albums if album.artist.name == artist_name]
			artist_album_ids = [album.ids for album in artist_albums]
			print(f"{artist_name} Albums: {artist_album_ids}")

run = lyrics()
run.get_artist_ids()
run.album_list()
run.test()