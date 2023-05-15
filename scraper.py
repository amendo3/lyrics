

# outdated shit method



import requests, re
from bs4 import BeautifulSoup

def getHTMLdocument():
	url = 'http://genius.com/songs/70324'
	page = requests.get(url)
	html = BeautifulSoup(page.text, "html.parser")
	[h.extract() for h in html('script')]
	lyrics = html.find("div", class_=re.compile('^lyrics$|Lyrics__Root')).get_text()
	print(lyrics)

getHTMLdocument()

# lyrics = soup.find(id="lyrics-root")
# print(lyrics.pretti


# path = 'https://genius.com/songs/70324'

# def lyrics(self):
# 	response = requests.get(path)
# 	html_document = response.text

# 	html = BeautifulSoup(html_document, 'html.parser')
# 	div = html.find("div", class_=re.compile('^lyrics$|Lyrics__Root'))
# 	if div is None:
# 		if self.verbose:
# 			print("Couldn't find the lyrics section. "
# 				"Please report this if the song has lyrics.\n"
# 				"Song URL: https://genius.com/songs/70324")

# 	blocklist = ['style', 'script', 'span']
# 	text = [t for t in div.find_all(string=True) if t.parent.name not in blocklist]

# 	print(text)

	# with open('song.txt', 'w') as song_text:
	# 	song_text.write(lyrics)


	# if self.remove_section_headers or remove_section_headers:
	# 	lyrics = re.sub(r'(\[.*?\])*', '', lyrics)
	# 	lyrics = re.sub('\n{2}', '\n', lyrics)
	# return lyrics.strip("\n")

# lyrics(path)