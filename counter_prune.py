import json
# import argparse
from pprint import pprint
import xlsxwriter

"""
parser = argparse.ArgumentParser()
parser.add_argument('query')
args = parser.parse_args()
"""

exclude_left = ['məli', 'malı', 'mək', 'maq']

f = open('data/task1.json')
d = json.load(f)
k = list(d.keys())

workbook = xlsxwriter.Workbook('data_pruned.xlsx')

for key in k:
	try:
		l = d[key]['Lines']
	except KeyError:
		continue

	results = dict()

	for r in l:
		try:
			word = r['Kwic'][0]['str']
			if word.endswith(key):
				#print('excluding no following letter')
				continue
			left = [ldict['str'] for ldict in r['Left']]
			for lw in left:
				if any(x in lw for x in exclude_left):
					#print('found excluded key')
					raise ValueError
			results[word] = results.get(word, 0) + 1
		except KeyError:
			continue
		except ValueError:
			continue

	if not results:
		continue

	worksheet = workbook.add_worksheet(key)

	row = 0
	sorted_keys = sorted(results, key=results.get, reverse=True)

	for skey in sorted_keys:
		worksheet.write(row, 0, skey)
		worksheet.write(row, 1, results[skey])
		row += 1

workbook.close()
f.close()