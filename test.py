import requests, csv, api_key, reader, os
from bs4 import BeautifulSoup

client_access_token = api_key.your_client_access_token


artist = []
ids = []
albums_ids = []
albums_name_list = []
albums_release_date = []
songs_release_date = []
tracklist_urls = []
search_term = None
artist_id_term = None
primary_artist_id = None
primary_artist_name = None

def fileOpener():
	file = open('csv.csv')
	fileReader = csv.DictReader(file, ['name'])

	for row in fileReader:
		artist.append(row['name'])

def artistID(list):
	print('Getting api url and artist IDs...')
	for x in list:
		search_term = x
		genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"

		# print(genius_search_url)
		response = requests.get(genius_search_url)
		json_data = response.json()
		
		for hit in json_data['response']['hits']:
			if hit['result']['primary_artist']['name'] == search_term:
				primary_artist_id = hit['result']['primary_artist']['id']
				ids.append(primary_artist_id)
				break


def albumList(list):
	print('Getting public api url and album lists...')
	for y in list:
		artist_id_term = y
		public_url_albums = f"http://genius.com/api/artists/{artist_id_term}/albums?per_page=50/"

		response = requests.get(public_url_albums)
		album_json_data = response.json()

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


		# this is commented out right now because it was a really poor way of getting every album that
		# appeared and not missing any. 


		# for albums in album_json_data['response']['albums']:
		# 	i = 0
		# 	while i < 50:
		# 	# if albums['artist']['id'] == artist_id_term:
		# 		album_id = albums['api_path']
		# 		albums_ids.append(album_id)
		# 		albums_name = albums['name']
		# 		albums_name_list.append(albums_name)
		# 		albums_date = albums['release_date_components']
		# 		albums_release_date.append(albums_date)
		# 		break

		

def songList(list):
	print('Getting public api url for each specific album...')
	for g in list:
		album_id_term = g
		public_url_tracklist = f"http://genius.com/api{album_id_term}/tracks"
		tracklist_urls.append(public_url_tracklist)
		


		



		# for i in range(10):
			# full_title = json_data['response']['hits'][i]['result']['full_title']
			# print(full_title)
			# release_date = json_data['response']['hits'][i]['result']['release_date_components']
			# print(release_date)
			# song_path = json_data['response']['hits'][i]['result']['path']
			# print(song_path)
			# song_api_path = json_data['response']['hits'][i]['result']['api_path']
			# print(song_api_path)
			# artist_id = json_data['response']['hits'][i]['result']['primary_artist']['id']
			


			# Both of these are not allowed within my scope: (will need to scrape)

			# genius_album_data = f"http://api.genius.com/artists/:{artist_id}/albums"
			# genius_album_url = f"http://api.genius.com/artists/{album_id}/tracks"
			# print(genius_album_data)
			# genius_public_api = f"http://genius.com/api/artists/:{artist}"



		# can add a if statement here to check if the name from the csv file actually matches the primary artist
		# listed on genius

		# can also add a check for song's lyric-state being complete or not


fileOpener()
artistID(artist)
albumList(ids)

songList(albums_ids)


length2 = len(albums_ids)
print('length of album_ids ' + str(length2))
length = len(tracklist_urls)
print('length of tracklist_urls ' + str(length))
# songList(albums_ids)
# print('The below information is for ' + str(artist) + 'with ID #: ' + str(ids))
# print('The album IDs are as follows: ' + str(albums_ids))
# print('The Album Names are as follows: ' + str(albums_name_list))
# print('The Album Release Dates are as follows: ' + str(albums_release_date))
