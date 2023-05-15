

# first time trying classes with this but not the best file. test2.py is the best rn





# import modules required, as well as auxillary files with function necessary
import requests, csv, api_key, reader, os
from bs4 import BeautifulSoup


class GeniusScraper():
	def __init__(self):
		self.access_token = api_key.token
		self.artist = []
		self.ids = []
		self.albums_ids = []
		self.albums_name_list = []
		self.albums_release_date = []
		self.artists_name_list = []
		self.tracklist_urls = []
		self.artist_id_term = None
		self.primary_artist_id = None
		self.primary_artist_name = None
		self.search_term = None

	def file_opener(self):
		file = open('csv.csv')
		fileReader = csv.DictReader(file, ['name'])

		for row in fileReader:
			self.artist.append(row['name'])

	def artist_ID(self, artist):
		print('artistID: Getting api url and artist IDs...')
		for artists in artist:
			self.search_term = artists
			genius_search_url = f"http://api.genius.com/search?q={self.search_term}&access_token={self.access_token}"
			response = requests.get(genius_search_url)
			json_data = response.json()

			for hit in json_data['response']['hits']:
				if hit['result']['primary_artist']['name'] == self.search_term:
					self.primary_artist_id = hit['result']['primary_artist']['id']
					self.ids.append(self.primary_artist_id)
					self.primary_artist_name = hit['result']['primary_artist']['name']
					self.artists_name_list.append(self.primary_artist_name)

					# print('Primary Artist ID: ' + self.primary_artist_id)
					# print('IDS: ' + self.ids)
					# print('Primary Artist ID: ' + self.primary_artist_name)
					# print('Artist Name List: ' + self.artist_name_list)
					break

	def album_list(self, ids):
		print('albumList: Getting public api url and album lists...')
		for artist_id in ids:
			self.artist_id_term = artist_id
			public_url_albums = f"http://genius.com/api/artists/{self.artist_id_term}/albums?per_page=50/"

			print('Public URL Albums: ' + public_url_albums)
			response2 = requests.get(public_url_albums)
			album_json_data = response2.json()

			for albums in album_json_data['response']['albums']:
				if albums['_type'] == "album":
					album_id = albums['api_path']
					self.albums_ids.append(album_id)
					albums_name = albums['name']
					self.albums_name_list.append(albums_name)
					albums_date = albums['release_date_components']
					self.albums_release_date.append(albums_date)
				else:
					break

	def song_list(self, albums_ids):
			print('songList: Getting public api url for each specific album and tracklist...')
			for album_id in albums_ids:
				album_id_term = album_id
				public_url_tracklist = f"http://genius.com/api{album_id_term}/tracks"
				self.tracklist_urls.append(public_url_tracklist)

	def createArtistFolder(self, artists_name_list, albums_name_list):
		for artist_name in artists_name_list:
			artist_name_term = str(artist_name)
			parent_dir = "/Users/amendo/repos/lyrics/files"
			path = os.path.join(parent_dir, artist_name_term)

			try:
				os.mkdir(path)
			except OSError as error:
				print(error)

		for album_name in albums_name_list:
			album_name_term = str(album_name)
			parent_dir2 = f"/Users/amendo/repos/lyrics/files/{artist_name_term}"
			path2 = os.path.join(parent_dir2, album_name_term)

			try:
				os.mkdir(path2)
			except OSError as error:
				print(error)

	def scrape(self):
		self.file_opener()
		self.artist_ID(self.artist)
		self.album_list(self.ids)
		self.song_list(self.albums_ids)
		self.createArtistFolder(self.artists_name_list, self.albums_name_list)

scraper = GeniusScraper()
scraper.scrape()


