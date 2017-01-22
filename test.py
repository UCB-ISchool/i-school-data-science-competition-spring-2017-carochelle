from pprint import pprint
import re
import urllib.request as req

def new_search(decoded):
	text = decoded[redirect + 9:]
	new_entry = re.search('[A-Z]', text)
	letter = new_entry.group(0)
	entry_start = text.find(letter) # 46 / 9 / 65
	entry_end = re.search("[^a-zA-Z.\d\s:]", text[entry_start:]) # issue with Bündchen
	end_symbol = entry_end.group(0)
	end = text.find(end_symbol, entry_start)
	name = text[entry_start: end]
	name = name.replace(' ', '%20')

	response = req.urlopen(endpoint + "?action=query&titles="+ name + "&prop=revisions&rvprop=content&format=json").read()
	decoded = response.decode('utf-8')
	return decoded

endpoint = 'https://en.wikipedia.org/w/api.php'

# took out BC ppl and entries that were not just 1 person (Wright Brothers)


count = 0		

response = req.urlopen(endpoint + "?action=query&titles="+ 'Pope%20John%20Paul%20II' + "&prop=revisions&rvprop=content&format=json").read()
decoded = response.decode('utf-8')

		# check if the page is redirected to another
redirect = decoded.find('#REDIRECT')
redirect2 = decoded.lower().find('#redirect')
redirect = redirect + redirect2
if redirect > -1:
	decoded = new_search(decoded)
		
spouse_word = decoded.find('^spouse')
text = decoded[spouse_word:]
marriage_start = text.lower().find('{marriage')
count_marriage = 0
list_of_spouses = []


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

num_divorces = decoded.count('divorce')
if num_divorces > 0 and count_divorces == 0 and len(list_of_spouses) > 0:
	count_divorces = 1

results =(('marilyn', count_marriage, count_divorces, list_of_spouses))
print(results)


#with open('marilyn.json', 'r') as f:
#	text = f.read()
#soup = BeautifulSoup(text, 'html.parser')
#print(soup.prettify())
#print(soup.body)