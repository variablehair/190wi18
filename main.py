from login import tom_username, tom_password
import requests
import pprint #for testing
import json
import urllib.parse

root_url = 'https://the.sketchengine.co.uk'
base_url='%s/bonito/run.cgi/' % root_url

login_url = 'https://the.sketchengine.co.uk/login/'
logindata = {'username' : tom_username, 'password' : tom_password,'submit' : 'ok'}

# query = '[lemma=".*dir.*"]'
attrs = dict(corpname = 'preloaded/turkic_az', q = 'q[word="dir"]', pagesize = '94267206', format = 'json')

s = requests.Session()
s.auth = (tom_username, tom_password)
s.get(login_url)
r = s.post(login_url,data=logindata)

encoded_attrs=urllib.parse.urlencode(attrs)
url = base_url + 'view'
r = s.get(url, params = attrs)
json_obj = r.json()
with open('data.txt', 'w') as outfile:
	json.dump(json_obj, outfile)