from login import tom_username, tom_password
import requests
import pprint #for testing
import json
import urllib.parse
import time
# import argparse

""" 
parser = argparse.ArgumentParser()
parser.add_argument('query')
args = parser.parse_args()
"""

root_url = 'https://the.sketchengine.co.uk'
base_url='%s/bonito/run.cgi/' % root_url

login_url = 'https://the.sketchengine.co.uk/login/'
logindata = {'username' : tom_username, 'password' : tom_password,'submit' : 'ok'}

qlist = []
queries = open('task1inc.txt', encoding='utf-8')
for line in queries:
    qlist.append(line.replace('\n', ''))

results = {}
for query in qlist:
	fquery = str('q[word=".*' + query + '.*"]')
	attrs = dict(corpname = 'preloaded/turkic_az', q = fquery, pagesize = '94267206', format = 'json')

	s = requests.Session()
	s.auth = (tom_username, tom_password)
	s.get(login_url)
	r = s.post(login_url,data=logindata)

	encoded_attrs=urllib.parse.urlencode(attrs)
	url = base_url + 'view'
	r = s.get(url, params = attrs)
	json_obj = r.json()
	results[query] = json_obj

	print(str(len(results)) + " complete.\n")

	time.sleep(20)

with open('data/task1j.json', mode='w', encoding='utf-8') as outfile:
	json.dump(results, outfile)