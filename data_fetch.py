from login import tom_username, tom_password
import requests
import json
import urllib.parse
import time

MAX_SAMPLES = 100

root_url = 'https://the.sketchengine.co.uk'
base_url='%s/bonito/run.cgi/' % root_url

login_url = 'https://the.sketchengine.co.uk/login/'
logindata = {'username' : tom_username, 'password' : tom_password,'submit' : 'ok'}

qlist = []
queries = open('task1clean.txt', encoding='utf-8')
for line in queries:
    qlist.append(line.replace('\n', ''))

s = requests.Session()
s.auth = (tom_username, tom_password)
s.get(login_url)
url = base_url + 'view'

#results = {}

api_log = open('api_log.txt', encoding='utf-8', mode='w')

for query in qlist:
	pagenum = 1
	fquery = str('q[word=".*' + query + '.*"]')
	attrs = dict(corpname = 'preloaded/turkic_az', q = fquery, pagesize = '1000', format = 'json', fromp=pagenum, r='r1000')
	curr_results = list()

	r = s.post(login_url,data=logindata)

	encoded_attrs=urllib.parse.urlencode(attrs)

	r = s.get(url, params = attrs)
	curr_res_dict = r.json()

	try:
		e = (curr_res_dict['error'])
		api_log.write('ERROR on ' + str(query) + ':\t' + str(e) + '\n')
		continue
	except KeyError:
		pass

	curr_results = curr_res_dict['Lines']
	try:
		total_pages = curr_res_dict['numofpages']
	except KeyError:
		total_pages = 1
	api_log.write(query + ' page ' + str(pagenum) + 'done, len = ' + str(len(curr_results)) + '\n')			
	
	if total_pages > 1:
		while pagenum < MAX_SAMPLES:
			pagenum += 1
			attrs['fromp'] = pagenum
			r = s.get(url, params=attrs)
			curr_res_dict = r.json()
			curr_results = curr_results + curr_res_dict['Lines']
			api_log.write(query + ' page ' + str(pagenum) + 'done, len = ' + str(len(curr_results)) + '\n')			
			time.sleep(10)
			if pagenum % 25 == 0:
				time.sleep(60)
				print(str(pagenum))

	with open('data/temp/' + query + '100.json', mode='w', encoding='utf=8') as f:
		json.dump(curr_results, f)
	curr_results = []

	time.sleep(120)

api_log.close()