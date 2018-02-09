import subprocess
import counter
import main

qlist = []
with open('task1clean.txt', encoding='utf-8') as queries:
    for line in queries:
        qlist.append(line.replace('\n', ''))

for query in qlist:
    main.fetch_query(query)

for query in qlist:
    counter.countdata(query)
