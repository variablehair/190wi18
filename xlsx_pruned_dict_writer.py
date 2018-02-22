import xlsxwriter

with open('pruned_dict_entries.txt', encoding='utf-8') as f:
    lines = f.readlines()
    tuple_list = []
    for line in lines:
        sl = line.split('\t')
        tuple_list.append((sl[0], sl[-1]))

results = {}
for tup in tuple_list:
    tup_results = results.get(tup[0], {})
    tup_results[tup[1]] = tup_results.get(tup[1], 0) + 1
    results[tup[0]] = tup_results

workbook = xlsxwriter.Workbook('pruned_dict_entries.xlsx')
worksheet = workbook.add_worksheet('Pruned Entries')

row = 0
for r in results:
    curr_dict = results[r]
    for key in curr_dict:
        worksheet.write(row, 0, r)
        worksheet.write(row, 1, key)
        worksheet.write(row, 2, curr_dict[key])
        row += 1

workbook.close()