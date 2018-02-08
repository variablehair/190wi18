import json
# import argparse
from pprint import pprint
import xlsxwriter

"""
parser = argparse.ArgumentParser()
parser.add_argument('query')
args = parser.parse_args()
"""

f = open('data/task1.json')
d = json.load(f)
k = list(d.keys())

workbook = xlsxwriter.Workbook('data.xlsx')

for key in k:
	try:
		l = d[key]['Lines']
	except KeyError:
		continue

	results = dict()

	for r in l:
		try:
			word = r['Kwic'][0]['str']
			results[word] = results.get(word, 0) + 1
		except KeyError:
			continue

	worksheet = workbook.add_worksheet(key)

	row = 0

	for result in results.keys():
		row += 1
		worksheet.write(row, 0, result)
		worksheet.write(row, 1, results[result])

workbook.close()