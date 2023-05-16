# import statements:
# requests for getting json data
# api_key is .gitignore'd so that it will not be public facing and can be called as var
# reader for accessing csv data
# os for creating folders that organize the artist, albums, and songs
# re gets used during scrape function afaik, selecting Lyrics__Container div
# csv for csv data stuff

import requests, api_key, reader, os, re, csv
from bs4 import BeautifulSoup

class getLyrics():
	def __init__(self):
		self.artist1 = []
		self.artist2 = []
		self.token = api_key.token
		self.ids1 = []
		self.artists_name_list1 = []
		self.albums_ids1 = []
		self.albums_name_list1 = []
		self.albums_release_date1 = []
		self.tracklist_urls1 = []
		self.songs_ids1 = []
		self.songs_titles1 = []
		self.songs_dates1 = []



	def artist_simple(self):
		# really simple method for getting the artist name one at a time. probably not hard to 
		# get the csv file working and doing all at once, but I want to move forward and get
		# this working at least
		name = input('Enter artist name: ')
		self.artist1.append(name)

	def artist_complex(self):
		# more complex method that will take the full list of artists and run through the rest
		# of the functions for each one. at this point this function works flawlessly at reading
		# the csv and appending to list, the latter stuff with actually iterating each function
		# for the specific artist, finishing, moving to the next artist, etc. is not fully done
		file = open('artists.csv')
		fileReader = csv.DictReader(file, ['name'])

		for row in fileReader:
			self.artist2.append(row['name'])

	def artistFolder_simple(self, artist1):
		# this function will be the same for both above methods so far, because this is just
		# creating a folder for each with their specific names
		for people in artist1:
			name = str(people)
			parent_dir = "/Users/amendo/repos/lyrics/files"
			path = os.path.join(parent_dir, name)

			try:
				os.mkdir(path)
			except OSError as error:
				print(error)

	def artistFolder_complex(self, artist2):
		# this function will be the same for both above methods so far, because this is just
		# creating a folder for each with their specific names
		for people in artist2:
			name = str(people)
			parent_dir = "/Users/amendo/repos/lyrics/files"
			path = os.path.join(parent_dir, name)

			try:
				os.mkdir(path)
			except OSError as error:
				print(error)

	def artist_id_simple(self, artist1):
		# this function goes through the artist1 list (which at this point is one name) to create
		# a url for the genius api link, which then can be accesses using the requests module to
		# receive json data and help us get artist ids, which are used for album ids and song ids.
		for names in artist1:
			id_search_term = names
			genius_search_url = f"http://api.genius.com/search?q={id_search_term}&access_token={self.token}"
			response = requests.get(genius_search_url)
			json_data = response.json()

			for hit in json_data['response']['hits']:
				if hit['result']['primary_artist']['name'] == id_search_term:
					primary_artist_id = hit['result']['primary_artist']['id']
					self.ids1.append(primary_artist_id)
					primary_artist_name = hit['result']['primary_artist']['name']
					self.artists_name_list1.append(primary_artist_name)

					break

	def album_list_simple(self, ids1):
		# this function is taking the list of ids(1 in this case since it's simple) and making
		# another http request in order to get the ids for albums and extra info. it's done this
		# way (even though it might be possible through just the artist api link) because there are
		# more specific api links to albums pages. 
		for artist_id in ids1:
			artist_id_term = artist_id
			public_url_albums = f"http://genius.com/api/artists/{artist_id_term}/albums?per_page=50/"

			response = requests.get(public_url_albums)
			album_json_data = response.json()

			for albums in album_json_data['response']['albums']:
				if albums['_type'] == "album":
					album_id = albums['api_path']
					self.albums_ids1.append(album_id)
					albums_name = albums['name']
					self.albums_name_list1.append(albums_name)
					albums_date = albums['release_date_for_display']
					self.albums_release_date1.append(albums_date)

				else:
					print('ALBUM_LIST ERROR')
					break

	def song_list_simple(self, albums_ids1):
		# this function takes the album ids just gathered and runs through them with another api
		# link in order to get tracklists for each album. I don't think this will change from simple
		# to complex but it might once I go further
		for aid in albums_ids1:
			album_id_term = aid
			public_url_tracklist = f"http://genius.com/api{album_id_term}/tracks"
			
			response = requests.get(public_url_tracklist)
			tracklist_json_data = response.json()

			for tracks in tracklist_json_data['response']['tracks']:
				if tracks['song']['_type'] == "song" and tracks['song']['lyrics_state'] == "complete":
					songs_id = tracks['song']['api_path']
					self.songs_ids1.append(songs_id)
					full_title = tracks['song']['full_title']
					self.songs_titles1.append(full_title)
					songs_date = tracks['song']['release_date_with_abbreviated_month_for_display']
					self.songs_dates1.append(songs_date)

	def write_lists_to_files(self, *lists):
		for i, lst in enumerate(lists):
			with open(f'list_{i+1}.txt', 'w') as f:
				for item in lst:
					f.write(str(item) + '\n')

	def program_run(self):
		self.artist_simple()
		self.artistFolder_simple(self.artist1)
		self.artist_id_simple(self.artist1)
		self.album_list_simple(self.ids1)
		self.song_list_simple(self.albums_ids1)

		self.write_lists_to_files(self.songs_ids1)

run = getLyrics()
run.program_run()



