from login import tom_username, tom_password
import requests
import json
import urllib.parse
import time

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
	attrs = dict(corpname = 'preloaded/turkic_az', q = fquery, pagesize = '1000', format = 'json', async=0, fromp=pagenum)
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
	total_pages = curr_res_dict['numofpages']
	api_log.write(query + ' page ' + str(pagenum) + 'done, len = ' + str(len(curr_results)) + '\n')			
	
	if total_pages > 1:
		while pagenum <= total_pages:
			pagenum += 1
			attrs['fromp'] = pagenum
			r = s.get(url, params=attrs)
			curr_res_dict = r.json()
			curr_results = curr_results + curr_res_dict['Lines']
			api_log.write(query + ' page ' + str(pagenum) + 'done, len = ' + str(len(curr_results)) + '\n')			
			time.sleep(20)
			if pagenum % 25 == 0:
				time.sleep(120)
				print(str(pagenum))
			if pagenum % 200 == 0 or pagenum == total_pages:
				with open('data/temp/' + query + str(pagenum) +'.json', mode='w', encoding='utf=8') as f:
					json.dump(curr_results, f)
				curr_results = []

	with open('data/temp/' + query + str(pagenum) +'.json', mode='w', encoding='utf=8') as f:
		json.dump(curr_results, f)

#	api_log.write('FINISHED ' + query + str(len(results)) + '\n')			
#	print(str(len(results)) + '\n')

	time.sleep(1200)

#with open('data/task1j.json', mode='w', encoding='utf-8') as outfile:
#	json.dump(results, outfile)

api_log.close()