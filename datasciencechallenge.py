import urllib.request as req
import json
import urllib.parse as up
import csv
from pprint import pprint
import re

endpoint = 'https://en.wikipedia.org/w/api.php'

def new_search(decoded):
	text = decoded[redirect + 9:]
	new_entry = re.search('[A-Z]', text)
	letter = new_entry.group(0)
	entry_start = text.find(letter) # 46 / 9 / 65
	entry_end = re.search("[^a-zA-Z.\d\s:]", text[entry_start:])
	end_symbol = entry_end.group(0)
	end = text.find(end_symbol, entry_start)
	name = text[entry_start: end]
	name = name.replace(' ', '%20')
	response = req.urlopen(endpoint + "?action=query&titles="+ name + "&prop=revisions&rvprop=content&format=json").read()
	decoded = response.decode('utf-8')
	return decoded


# took out BC ppl and entries that were not just 1 person (Wright Brothers)

titles = []
with open('celebrities_100.csv', encoding='utf-8') as csvfile:
	reader = csv.reader(csvfile)
	for line in reader:
		name = line[1]
		if name[-1] == ' ':
			name = name[:-1]
		name = name.replace(' ', '%20')
		titles.append(name)

count = 0		
with open('data.csv', 'w', newline='') as csvfile:
	celebwriter = csv.writer(csvfile, delimiter = ',')
	for entry in titles:
		results = []
		count_marriage = 0
		list_of_spouses = []
		if entry == "Name":
			continue
		response = req.urlopen(endpoint + "?action=query&titles="+ entry + "&prop=revisions&rvprop=content&format=json").read()
		decoded = response.decode('utf-8')

		# check if the page is redirected to another
		redirect = decoded.find('#REDIRECT')
		if redirect > -1:
			decoded = new_search(decoded)
		
		spouse_word = decoded.find('spouse')
		text = decoded[spouse_word:]
		marriage_start = text.lower().find('{marriage')

		if marriage_start == - 1:
			if spouse_word >= 0:
				count_marriage = 1
				name_start = re.search('[A-Z]', text[6:])
				letter = name_start.group(0)
				name_start = text.find(letter)
				name_end = re.search("[^a-zA-Z\d\s:]", text[name_start:])
				end_symbol = name_end.group(0)
				end = text.find(end_symbol, name_start)
				name = text[name_start: end]
				list_of_spouses.append(name)
				print()

		count_divorces = text.count('end=div')
		count_divorces2 = text.count ('reason=divorced')
		count_divorces = count_divorces + count_divorces2
		while marriage_start > 0: # entered three times
			count_marriage += 1
			text = text[marriage_start + 6:]
			name_start = re.search('[A-Z]', text)
			letter = name_start.group(0)
			name_start = text.find(letter) # 36
			#name_end = re.search("[^a-zA-Z.\d\s:]", text[name_start:])
			name_end = re.search("[^\w\s]", text[name_start:])
			end_symbol = name_end.group(0)
			end = text.find(end_symbol, name_start)
			name = text[name_start: end]
			list_of_spouses.append(name)
			text = text[marriage_start:]
			marriage_start = text.lower().find('{marriage')
		
		entry = entry.replace('%20', " ")

		results.append((entry, count_marriage, count_divorces, list_of_spouses))
		spouses = ""
		for item in list_of_spouses:
			spouses = spouses + item + ', '
		spouses = spouses[:-2]
		string = entry + "," + str(count_marriage) + "," + str(count_divorces) + "," + spouses
		celebwriter.writerow(string)







