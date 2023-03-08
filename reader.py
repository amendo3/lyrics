import csv

lines = []
artists = []
artistFile = open('artists.csv')
csvReader = csv.DictReader(artistFile, ['number', 'name'])
#csvData = list(csvReader)

for row in csvReader:
	if csvReader.line_num == 1:
		artists.append(row['name'])
	elif csvReader.line_num == 2:
		artists.append(row['name'])
	elif csvReader.line_num == 3:
		artists.append(row['name'])
	elif csvReader.line_num == 4:
		artists.append(row['name'])
	elif csvReader.line_num == 5:
		artists.append(row['name'])
	else:
		print('logic is surely fucked')

for row in csvReader:
	lines.append(row['name'])


print(lines)
print(artists)