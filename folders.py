import requests, api_key, reader, os, re, csv
from bs4 import BeautifulSoup

class folderMaker():
	def __init__(self):
		self.artist = []

	def file_opener(self):
		file = open('artists.csv')
		fileReader = csv.DictReader(file, ['name'])

		for row in fileReader:
			self.artist.append(row['name'])



	def createFolder(self, artist):
		for people in artist:
			name = str(people)
			parent_dir = "/Users/amendo/repos/lyrics/files"
			path = os.path.join(parent_dir, name)

			try:
				os.mkdir(path)
			except OSError as error:
				print(error)


	def run(self):
		self.file_opener()
		
		self.createFolder(self.artist)

test = folderMaker()
test.run()