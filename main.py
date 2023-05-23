# import statements
import requests, api_key, os, re, csv
from bs4 import BeautifulSoup

# class declarations - each are templates for instances to be created that will store various data points
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

class Songs():
	def __init__(self, artist, name = None, ids = None, date = None, lyrics = None):
		self.artist = artist
		self.name = name
		self.ids = ids
		self.date = date
		self.lyrics = lyrics

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
				print(f"artistReader - Read artist: {artist_name}")

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
					print(f"artistIdScraper - Scraped artist ID for '{id_search_term}': {primary_artist_id}")
					break

class albumIdScraper():
	def __init__(self, artists_list):
		self.artists_to_get_album_ids = artists_list
		self.albums = []


		def scraper(self):
			for artist in self.artists_to_get_album_ids:
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
					print(f"albumIdScraper - Scraped album ID for '{album_name}': {album_id}")


				else:
					print('ALBUM LIST ERROR')
					break

class songListScraper():
	def __init__(self, albums):
		self.albums = albums

		self.songs_list = []

		def scraper(self):
			for album in self.albums:
			song_id_term = album.ids
			public_url_tracklist = f"http://genius.com/api{song_id_term}/tracks"

			print(public_url_tracklist)

			response = requests.get(public_url_tracklist)
			tracklist_json_data = response.json()


			for tracks in tracklist_json_data['response']['tracks']:
				if tracks['song']['_type'] == "song" and tracks['song']['lyrics_state'] == "complete":
					songs_id = tracks['song']['api_path']
					full_title = tracks['song']['full_title']
					songs_date = tracks['song']['release_date_with_abbreviated_month_for_display']


					songs = Songs(album.artist, full_title, songs_id, songs_date)
					self.songs_list.append(songs)

				else:
					error_url = f"http://genius.com/api{song_id_term}/tracks"
					print(f"SONG LIST ERROR - {error_url}")
					continue

class createFolders():
	def __init__(self, artists):
		self.artists = artists
		self.parent_dir = "/Users/amendo/repos/lyrics/files"


	def artistFolder(self):
		for artist in self.artists:
			artist_name = artist.name
			artist_dir = os.path.join(self.parent_dir, artist_name)

			try:
				os.mkdir(artist_dir)
				print(f"createFolders - Created folder: {artist_dir}")
			except OSError as error:
				print(error)


class logic():
	def __init__(self):
		self.artist_reader = artistReader('artists.csv')
		self.artists = self.artist_reader.read_artists()

		self.artist_id_scraper = artistIdScraper(self.artists)

		self.album_id_scraper = albumIdScraper(self.artists)

		# self.song_list_scraper = None



		def get_artist_ids(self):
			self.artist_id_scraper.scraper()

		def get_album_ids(self):
			self.album_id_scraper.scraper()

		def get_song_list(self):
			self.song_list_scraper = songListScraper(self.album_id_scraper.albums)
			self.song_list_scraper.scraper()

		def create_folders(self):
			folder_creator = createFolders(self.artists)
			folder_creator.artistFolder()

run = logic()
run.get_artist_ids()
run.get_album_ids()
run.get_song_list()
run.create_folders()










