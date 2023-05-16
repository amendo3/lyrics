import requests, api_key, reader, os, re, csv
from bs4 import BeautifulSoup

class getLyrics():
	def __init__(self):
		self.artist1 = []
		self.artist2 = []
		self.token = api_key.token
		self.ids = []
		self.artists_name_list = []
		self.albums_ids = []
		self.albums_name_list = []
		self.tracklist_urls = []
		self.song_ids = []
		self.song_titles = []
		self.song_dates = []

	def artist1(self):
		name = input('Enter artist name: ')
		self.artist1.append(name)

	def artist2(self):
		file = open('artists.csv')
		fileReader = csv.DictReader(file, ['name'])

		for row in fileReader:
			self.artist2.append(row['name'])

