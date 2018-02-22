import xlsxwriter
import json

workbook_dat = xlsxwriter.Workbook('dict_pruned_dative.xlsx')
with open('data/dative_pruned.json') as f:
    j_dat = json.load(f)

workbook_acc = xlsxwriter.Workbook('dict_pruned_accusative.xlsx')
with open('data/accusative_pruned.json') as f:
    j_acc = json.load(f)

for token in j_dat:
    worksheet = workbook_dat.add_worksheet(token)
    row = 0
    word_dict = j_dat[token]
    for word in word_dict:
        dat_dict = word_dict[word]
        for dat in dat_dict:
            worksheet.write(row, 0, word)
            worksheet.write(row, 1, dat)
            worksheet.write(row, 2, dat_dict[dat])
            row += 1
workbook_dat.close()

for token in j_acc:
    worksheet = workbook_acc.add_worksheet(token)
    row = 0
    word_dict = j_acc[token]
    for word in word_dict:
        acc_dict = word_dict[word]
        for acc in acc_dict:
            worksheet.write(row, 0, word)
            worksheet.write(row, 1, acc)
            worksheet.write(row, 2, acc_dict[acc])
            row += 1
workbook_acc.close()