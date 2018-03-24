import string
import re
import xlsxwriter
import json

INVALID_EXCEL_CHAR = r'[\[\]\:\*\?\/\\]'

with open('dict.txt', encoding='utf-8') as f:

    res = dict()
    curr = ''

    for l in f:
        line = l.split(' ')

        try:
            if line[0].isupper():
                curr = re.sub(r'\([^()]*\)', '', line[0])
                line = line[1:]

            for word in line:
                if word.islower() and '.' in word and not any([digit in word for digit in string.digits]):
                    word = re.sub(INVALID_EXCEL_CHAR, '', word)
                    rlist = res.get(word, [])
                    rlist.append(curr)
                    res[word] = rlist
                else:
                    raise IndexError

        except IndexError:
            continue

with open('../data/syncat.json', encoding='utf-8', mode='w') as f:
    json.dump(res, f)

workbook = xlsxwriter.Workbook('syntactic_category.xlsx')
for key in res:
    row = 0
    if len(res[key]) < 20:
        continue
    worksheet = workbook.add_worksheet(key)
    for entry in res[key]:
        worksheet.write(row, 0, entry)
        row += 1
workbook.close()