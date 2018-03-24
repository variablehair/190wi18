import sqlite3
import xlsxwriter
from operator import itemgetter

with open('task1clean.txt', encoding='utf-8') as f:
    token_list = f.readlines()

conn = sqlite3.connect('data/data100.db')

workbook = xlsxwriter.Workbook('task3_hapax.xlsx')

for token in token_list:
    c = conn.cursor()
    query = '''SELECT token FROM {0}'''.format(token)
    c.execute(query)
    
    total = 0
    hapax = 0
    found_words = dict()

    while True:
        row = c.fetchone()
        if row == None:
            break
        found_words[row[0]] = found_words.get(row[0], 0) + 1

    for word in found_words:
        num = found_words[word]
        total += num
        if num == 1:
            hapax += 1
    
    results_list = sorted(found_words.items(), key=itemgetter(1), reverse=True)
    
    worksheet = workbook.add_worksheet(token)
    
    row = 0
    worksheet.write(row, 0, 'Total hapax')
    worksheet.write(row, 1, 'Total tokens')
    
    row += 1
    worksheet.write(row, 0, hapax)
    worksheet.write(row, 1, total)
    worksheet.write(row, 2, str(hapax/total))

    row += 2
    for result in results_list:
        worksheet.write(row, 0, result[0])
        worksheet.write(row, 1, result[1])
        row += 1
