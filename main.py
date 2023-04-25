# import modules required, as well as auxillary files with function necessary
import requests, csv, api_key, reader, os
from bs4 import BeautifulSoup

#set variable for api token, pull real token from .gitignored api_key file
access_token = api_key.token

# global values being used
artist = []
ids = []
albums_ids = []
albums_name_list = []
albums_release_date = []
artist_name_list = []
tracklist_urls = []
artist_id_term = None
primary_artist_id = None
primary_artist_name = None
search_term = None

class fileSetup():
	def fileOpener():
		file = open('csv.csv')
		fileReader = csv.DictReader(file, ['name'])

		for row in fileReader:
			artist.append(row['name'])

	def artistID(list):
		print('artistID: Getting api url and artist IDs...')
		for x in list:
			search_term = x
			genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={token}"

			print('Genius Search Url: ' + genius_search_url)
			response = requests.get(genius_search_url)
			json_data = response.json()

			for hit in json_data['response']['hits']:
				if hit['result']['primary_artist']['name'] == search_term:
					primary_artist_id = hit['result']['primary_artist']['id']
					ids.append(primary_artist_id)
					primary_artist_name = hit['result']['primary_artist']['name']
					artist_name_list.append(primary_artist_name)

					print('Primary Artist ID: ' + primary_artist_id)
					print('IDS: ' + ids)
					print('Primary Artist ID: ' + primary_artist_name)
					print('Artist Name List: ' + artist_name_list)
					break

	def albumList(list):
		print('albumList: Getting public api url and album lists...')
		for y in list:
			artist_id_term = y
			public_url_albums = f"http://genius.com/api/artists/{artist_id_term}/albums?per_page=50/"

			print('Public URL Albums: ' + public_url_albums)
			response2 = requests.get(public_url_albums)
			album_json_data = response2.json()

			for albums in album_json_data['response']['albums']:
				if albums['_type'] == "album":
					album_id = albums['api_path']
					albums_ids.append(album_id)
					albums_name = albums['name']
					albums_name_list.append(albums_name)
					albums_date = albums['release_date_components']
					albums_release_date.append(albums_date)
				else:
					break

	def songList(list):
			print('songList: Getting public api url for each specific album and tracklist...')
			for z in list:
				album_id_term = z
				public_url_tracklist = f"http://genius.com/api{album_id_term}/tracks"
				tracklist_urls.append(public_url_tracklist)

	def createArtistFolder(list, nlist):
		for h in list:
			artist_name_term = str(h)
			parent_dir = "/Users/amendo/repos/lyrics/files"
			path = os.path.join(parent_dir, artist_name_term)

			try:
				os.mkdir(path)
			except OSError as error:
				print(error)

		for g in nlist:
			album_name_term = str(g)
			parent_dir2 = f"/Users/amendo/repos/lyrics/files/{artist_name_term}"
			path2 = os.path.join(parent_dir2, album_name_term)

			try:
				os.mkdir(path2)
			except OSError as error:
				print(error)



