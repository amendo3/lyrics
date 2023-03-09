import csv # get csv module in order to import the spreadsheet from this folder and get data from it (our
# artist names most importantly.)

# empty lists
lines = []
artists = []

#open the file with names and make DictReader object with "headers"
artistFile = open('artists.csv')
csvReader = csv.DictReader(artistFile, ['number', 'name'])

# for as many rows as are in the document, take the first column with header 'number' and append it to the empty
# lines index. same with second column header 'name' being appended to empty artists index.
for row in csvReader:
	lines.append(row['number'])
	artists.append(row['name'])

