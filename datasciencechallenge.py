import urllib.request as re
import json
import urllib.parse as up


response = re.urlopen("https://en.wikipedia.org/w/api.php?action=query&titles=Main%20Page&prop=revisions&rvprop=content&format=jsonfm").read()
decoded = response.decode('utf-8')
print(decoded)