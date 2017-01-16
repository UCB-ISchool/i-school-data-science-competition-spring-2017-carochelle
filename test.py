from pprint import pprint
import re
import urllib.request as req



endpoint = 'https://en.wikipedia.org/w/api.php'

response = req.urlopen(endpoint + "?action=query&titles=" + "Margaret%20Thatcher" + "&prop=revisions&rvprop=content&format=json").read()
decoded = response.decode('utf-8')

spouse_word = decoded.find('spouse')
text = decoded[spouse_word:]
results = []
count_marriage = 0
list_of_spouses = []
marriage_start = text.find('{marriage')
while marriage_start > 0: # entered three times
	count_marriage += 1
	text = text[marriage_start:]
	name_start = re.search('[A-Z]', text)
	letter = name_start.group(0)
	name_start = text.find(letter) # 46 / 9 / 65
	name_end = re.search("[^a-zA-Z\d\s:]", text[name_start:])
	end_symbol = name_end.group(0)
	end = text.find(end_symbol, name_start)
	name = text[name_start: end]
	list_of_spouses.append(name)
	text = text[marriage_start + 10:]
	marriage_start = text.find('{marriage')

if marriage_start == - 1:
	name_start = re.search('[A-Z]', text[6:])
	letter = name_start.group(0)
	name_start = text.find(letter)
	name_end = re.search("[^a-zA-Z\d\s:]", text[name_start:])
	end_symbol = name_end.group(0)
	end = text.find(end_symbol, name_start)
	name = text[name_start: end]
	list_of_spouses.append(name)

results.append(('maggie', count_marriage, list_of_spouses))
print(results)

#with open('marilyn.json', 'r') as f:
#	text = f.read()
#soup = BeautifulSoup(text, 'html.parser')
#print(soup.prettify())
#print(soup.body)