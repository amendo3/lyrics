import requests, api_key, reader, os, re, csv
from bs4 import BeautifulSoup

class testScrape():
	def __init__(self):
		self.token = api_key.token
		self.artist = []
		self.ids = []
		self.albums_ids = []
		self.artists_name_list = []
		self.albums_name_list = []
		self.albums_release_date = []
		self.artist_id_term = []
		self.tracklist_urls = []
		self.search_term = None

	def pick_artist(self):
		# really simple method to get a name, thinking it might be better to get 
		# something that works for each specific artist one at a time rather than 
		# starting out trying to import a csv list and iterate through all. this
		# should be much quicker to start and get right and then I can move to that
		name = input('Enter artist name: ')
		self.artist.append(name)

		print(name)

	def file_opener(self):
		file = open('artists.csv')
		fileReader = csv.DictReader(file, ['name'])

		for row in fileReader:
			self.artist.append(row['name'])

	def createArtistFolder(self, artist):
		for people in artist:
			name = str(people)
			parent_dir = "/Users/amendo/repos/lyrics/files"
			path = os.path.join(parent_dir, name)

			try:
				os.mkdir(path)
			except OSError as error:
				print(error)

	def artist_id(self, artist):
		print('artist_id: getting api url and artist id...')
		for artists in artist:
			self.search_term = artists
			genius_search_url = f"http://api.genius.com/search?q={self.search_term}&access_token={self.token}"
			response = requests.get(genius_search_url)
			json_data = response.json()

			print(genius_search_url)

			for hit in json_data['response']['hits']:
				if hit['result']['primary_artist']['name'] == self.search_term:
					primary_artist_id = hit['result']['primary_artist']['id']
					self.ids.append(primary_artist_id)
					primary_artist_name = hit['result']['primary_artist']['name']
					self.artists_name_list.append(primary_artist_name)

					break

			print('ids = ' + str(self.ids))
			print('artists_name_list = ' + str(self.artists_name_list))

	def album_list(self, ids):
		print('album_list: getting api url for album list...')
		for artist_id in ids:
			self.artist_id_term = artist_id
			public_url_albums = f"http://genius.com/api/artists/{self.artist_id_term}/albums?per_page=50/"

			print('Albums url: ' + public_url_albums)
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
					print('ALBUM_LIST ERROR')
					break

			print('albums_ids = ' + str(self.albums_ids))
			print('albums_name_list = ' + str(self.albums_name_list))
			print('albums_release_date = ' + str(self.albums_release_date))

	def song_list(self, albums_ids):
		print('songList: Getting public api url for each specific album and tracklist...')
		for aid in albums_ids:
			album_id_term = aid
			public_url_tracklist = f"http://genius.com/api{album_id_term}/tracks"
			self.tracklist_urls.append(public_url_tracklist)


		print(self.tracklist_urls)


	def get_html(self):
		url = 'http://genius.com/songs/70324'
		page = requests.get(url)
		html = BeautifulSoup(page.text, "html.parser")
		# [h.extract() for h in html('script')]
		# lyrics = html.find("div", class_=re.compile('^.*Lyrics__Container.*$')).get_text(separator='\n')
		# print(lyrics)

		for words in html.select('div[class^="Lyrics__Container"]'):
			for lines in words.select('i, b'):
				lines.unwrap()
			words.smooth()

			lyrics = words.get_text(strip=True, separator='\n')
			if lyrics:
				print(lyrics)

	def program(self):
		self.file_opener()
		self.createArtistFolder(self.artist)
		self.artist_id(self.artist)
		self.album_list(self.ids)
		self.song_list(self.albums_ids)


scrape = testScrape()
scrape.program()






