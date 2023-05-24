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
		self.songs_list = []

	def artistFolder(self, list):
		parent_dir = "/Users/amendo/repos/lyrics/files"

		for artist in list:
			artist_name = artist.name
			artist_dir = os.path.join(parent_dir, artist_name)

			try:
				os.mkdir(artist_dir)
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

	def song_list(self):
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


	def get_html(self):
		for song in self.songs_list[:10]:
			url = f"http://genius.com/songs/{song.ids}"
			page = requests.get(url)
			html = BeautifulSoup(page.text, "html.parser")

			for words in html.select('div[class^="Lyrics__Container"]'):
				for lines in words.select('i, b'):
					lines.unwrap()
				words.smooth()

				lyrics = words.get_text(strip=True, separator='\n')
				if lyrics:
					song.lyrics = lyrics

		self.artistFolder(self.artists)
		self.write_lyrics_to_files()

	def write_lyrics_to_files(self):
		parent_dir = "/Users/amendo/repos/lyrics/files"

		for song in self.songs_list[:10]:
			artist_name = song.artist.name
			album_name = song.name
			lyrics = song.lyrics

			if lyrics is None:
				continue

			artist_dir = os.path.join(parent_dir, artist_name)
			album_dir = os.path.join(artist_dir, album_name)

			os.makedirs(album_dir, exist_ok=True)

			filename = f"{album_name}.txt"
			filepath = os.path.join(album_dir, filename)

			with open(filepath, 'w') as file:
				file.write(lyrics)


	# def test(self):
	# 	# print([artist.name for artist in self.artists])
	# 	# print([artist.ids for artist in self.artists])

	# 	# for album in self.albums:
	# 	# 	print(album.ids)

	# 	# for artist in self.artists:
	# 	# 	artist_name = artist.name
	# 	# 	artist_albums = [album for album in self.albums if album.artist.name == artist_name]
	# 	# 	artist_album_ids = [album.ids for album in artist_albums]
	# 	# 	print(f"{artist_name} Albums: {artist_album_ids}")

		for song in self.songs_list:
			artist_name = song.artist.name
			song_name = song.name
			song_ids = song.ids
			song_date = song.date
			print(f"Artist: {artist_name}, Song: {song_name}, IDs: {song_ids}, Date: {song_date}")




run = lyrics()
run.get_artist_ids()
run.album_list()
run.song_list()
run.get_html()
# run.test()