import json
import argparse
from pprint import pprint
import xlsxwriter

parser = argparse.ArgumentParser()
parser.add_argument('query')
args = parser.parse_args()

try:
	data = json.load(open(str(args.query + ".json")))
except IOError:
	print(str('Error opening file ' + args.query))
	sys.exit(1)

l = data['Lines']
	
results = dict()

for r in l:
	word = r['Kwic'][0]['str']
	results[word] = results.get(word, 0) + 1
	
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()

row = 0

for key in results.keys():
    row += 1
    worksheet.write(row, 0, key)
    worksheet.write(row, 1, results[key])
    row += 1

workbook.close()