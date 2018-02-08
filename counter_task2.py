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

dat_acc_case = ['a', 'ə']
#, 'i', 'u', 'ü', 'ı'
prev_word_exclude = ['in', 'un', 'ün', 'ın']
end_of_sentence = ['.', '?', '!', '\n']
# and -1 = n

def process_dat_acc_case(token_list, results):
	next_l_token = None
	for l_token in token_list:
		if l_token in end_of_sentence:
			break
		elif len(l_token) <= 2:
			next_l_token = None
			continue
		elif next_l_token is None:
			next_l_token = l_token
			continue 

		if next_l_token[-1] in dat_acc_case:
			if next_l_token[-2] == 'n' and l_token[-2:] in prev_word_exclude:
				next_l_token = None
				continue
			dict_dat_acc = results.get(word, {})
			dict_dat_acc[next_l_token] = dict_dat_acc.get(next_l_token, 0) + 1
			results[word] = dict_dat_acc

f = open('data/task1.json')
d = json.load(f)
k = list(d.keys())

workbook = xlsxwriter.Workbook('data_task2.xlsx')

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
			left = [ldict['str'].split(' ') for ldict in r['Left']]
			left = [string for sublist in left for string in sublist]
			right = [rdict['str'].split(' ') for rdict in r['Right']]
			for lw in left:
				if any(x in lw for x in exclude_left):
					#print('found excluded key')
					raise ValueError
			
			left.reverse()

			process_dat_acc_case(left, results)
			process_dat_acc_case(right, results)	
					
		#except KeyError:
		#	continue 
		except ValueError:
			continue

	if not results:
		with open('all_results_pruned.txt', mode='w', encoding='utf-8') as outfile:
			outfile.write(key)
		continue

	worksheet = workbook.add_worksheet(key)
	row = 0

	for token in results:
		sorted_dat_acc_dict = sorted(results[token], key=results[token].get, reverse=True)
		for skey in sorted_dat_acc_dict:
			worksheet.write(row, 0, token)
			worksheet.write(row, 1, skey)
			worksheet.write(row, 2, results[token][skey])
			row += 1

workbook.close()
f.close()