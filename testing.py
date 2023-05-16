import requests, api_key, reader, os, re, csv
from bs4 import BeautifulSoup

class Artist():
	def __init__(self, name, ids=None):
		self.name = name
		self.ids = ids

class Album():
	def __init__(self, name = None, ids=None, date=None):
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
				# previous method
				# artist_name = row[0]
				# self.artists.append(artist_name)

				#new method
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
					# self.ids1.append(primary_artist_id)
					# primary_artist_name = hit['result']['primary_artist']['name']
					# self.artists_name_list1.append(primary_artist_name)
					artist.ids = primary_artist_id
					break

class lyrics():
	def __init__(self):
		self.artist_reader = artistReader('artists.csv')
		self.artists = self.artist_reader.read_artists()
		self.artist_id_scraper = artistIdScraper(self.artists)
		# self.artist_id_scraper.scraper(self.artists)
		# self.ids = self.artist_id_scraper.ids1


		self.albums_ids1 = []
		self.albums_names_list1 = []
		self.albums_release_date1 = []

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
		alb = self.artists

		for aid in alb:
			artist_id_term = aid
			public_url_albums = f"http://genius.com/api/artists/{artist_id_term}/albums?per_page=50/"

			response = requests.get(public_url_albums)
			album_json_data = response.json()

			for albums in album_json_data['response']['albums']:
				if albums['_type'] == "album":
					album = Album()

					album_id = albums['api_path']
					album.url_list = album_id
					self.albums_ids1.append(album_id)

					albums_name = albums['name']
					album.name = albums_names
					self.albums_name_list1.append(albums_name)

					albums_date = albums['release_date_for_display']
					album.date = albums_date
					self.albums_release_date1.append(albums_date)

				else:
					print('ALBUM LIST ERROR')
					break


	def test(self):
		# print(self.artists)
		# self.artistFolder(self.artists)
		# print(self.ids)
		print([artist.name for artist in self.artists])
		print([artist.ids for artist in self.artists])
		# instance1 = self.artists[0]
		# print(instance1.name)
		# print(instance1.ids)
		# instance2 = self.artists[2]
		# print(instance2.name)
		# print(instance2.ids)
		instance = Album()
		print(instance.ids)



run = lyrics()
run.get_artist_ids()
run.album_list()
run.test()