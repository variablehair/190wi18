import xlsxwriter
import json
from operator import itemgetter

workbook_dat = xlsxwriter.Workbook('dict_pruned_dative.xlsx')
with open('data/dative_pruned.json') as f:
    j_dat = json.load(f)

for token in j_dat:
    worksheet = workbook_dat.add_worksheet(token)
    row = 0
    word_dict = j_dat[token]
    for word in word_dict:
        tup_results = sorted(word_dict[word].items(), key=itemgetter(1), reverse=True)
        for tup in tup_results:
            worksheet.write(row, 0, word)
            worksheet.write(row, 1, tup[0])
            worksheet.write(row, 2, tup[1])
            row += 1
workbook_dat.close()

workbook_acc = xlsxwriter.Workbook('dict_pruned_accusative.xlsx')
with open('data/accusative_pruned.json') as f:
    j_acc = json.load(f)

for token in j_acc:
    worksheet = workbook_acc.add_worksheet(token)
    row = 0
    word_dict = j_acc[token]
    for word in word_dict:
        tup_results = sorted(word_dict[word].items(), key=itemgetter(1), reverse=True)
        for tup in tup_results:
            worksheet.write(row, 0, word)
            worksheet.write(row, 1, tup[0])
            worksheet.write(row, 2, tup[1])
            row += 1
workbook_acc.close()