# import statements
import requests, api_key, os, re, csv
from bs4 import BeautifulSoup

# class declarations - each are templates for instances to be created that will store various data points
class Artist():
	def __init__(self, name, ids= None):
		self.name = name
		self.ids = ids

class Album():
	def __init__(self, artist, name = None, ids = None, date = None, songs = None):
		self.artist = artist
		self.name = name
		self.ids = ids
		self.date = date
		self.songs = songs

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
				# print(f"artistReader - Read artist: {artist_name}")

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
					# print(f"artistIdScraper - Scraped artist ID for '{id_search_term}': {primary_artist_id}")
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
					# print(f"albumIdScraper - Scraped album ID for '{album_name}': {album_id}")

					album_songs = self.songListScraper(album_id)
					album.songs = album_songs
				else:
					print('ALBUM LIST ERROR')

			
					

	def songListScraper(self, album_id):
		song_list = []

		public_url_tracklist = f"http://genius.com/api{album_id}/tracks"
		response = requests.get(public_url_tracklist)
		tracklist_json_data = response.json()

		for track_data in tracklist_json_data['response']['tracks']:
			if track_data['song']['_type'] == "song" and track_data['song']['lyrics_state'] == "complete":
				song_id = track_data['song']['api_path']
				full_title = track_data['song']['full_title']
				song_date = track_data['song']['release_date_with_abbreviated_month_for_display']
				song_artist = track_data['song']['primary_artist']['name']

				song = Songs(song_artist, full_title, song_id, song_date)
				song_list.append(song)

			else:
				# error_url = f"http://genius.com/api{album_id}/tracks"
				# print(f"SONG LIST ERROR - {error_url}")
				continue

		return song_list


class createFolders():
	def __init__(self, albums):
		self.albums = albums
		self.parent_dir = "/Users/amendo/repos/lyrics/files"

	def artist_folder(self, artist_name):
		artist_dir = os.path.join(self.parent_dir, artist_name)

		try:
			os.mkdir(artist_dir)
			# print(f"createFolders - Created Folder: {artist_dir}")
		except OSError as error:
			print(error)

		return artist_dir

	def album_folder(self):
		for album in self.albums:
			artist_name = album.artist
			album_name = album.name

			artist_folder = self.artist_folder(artist_name)
			album_dir = os.path.join(artist_folder, album_name)

			try:
				os.mkdir(album_dir)
				# print(f"createFolders - Created Folder: {album_dir}")
			except OSError as error:
				print(error)

	def all_folders(self):
		self.ablum_folders()


class logic():
	def __init__(self):
		self.artist_reader = artistReader('artists.csv')
		self.artists = self.artist_reader.read_artists()

		self.artist_id_scraper = artistIdScraper(self.artists)

		self.album_id_scraper = albumIdScraper(self.artists)



	def get_artist_ids(self):
		self.artist_id_scraper.scraper()

	def get_album_ids(self):
		self.album_id_scraper.scraper()

	def create_folders(self):
		folder_creator = createFolders(self.artists)
		folder_creator.all_folders()

run = logic()
run.get_artist_ids()
run.get_album_ids()
run.create_folders()


# # Print Artists
# print("Artists:")
# for artist in run.artist_id_scraper.artists_to_scrape:
#     print(f"Artist Name: {artist.name}")
#     print(f"Artist ID: {artist.ids}")
#     print()

# # Print Albums
# print("Albums:")
# for album in run.album_id_scraper.albums:
#     print(f"Artist Name: {album.artist.name}")
#     print(f"Album Name: {album.name}")
#     print(f"Album ID: {album.ids}")
#     print(f"Release Date: {album.date}")
#     print()



# print("Albums:")
# for album in run.album_id_scraper.albums:
#     print(f"Artist Name: {album.artist.name}")
#     print(f"Album Name: {album.name}")
#     print(f"Album ID: {album.ids}")
#     print(f"Release Date: {album.date}")
#     print("Songs:")
#     for song in album.songs:
#         print(f"  Song ID: {song.ids}")
#         print(f"  Song Name: {song.name}")
#         print(f"  Song Date: {song.date}")
#         print(f"  Song Artist: {song.artist}")
#     print()







