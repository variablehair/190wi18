import os
import json
import sqlite3
import ast

datapath = 'data/temp/'
datadir = os.fsencode(datapath)
conn = sqlite3.connect('data/data100.db')

def process_raw_json(filename, tokenname, dbconn):
    c = dbconn.cursor()
    try:
        c.execute('''CREATE TABLE {} (token TEXT, left TEXT, right TEXT)'''.format(tokenname))
    except sqlite3.OperationalError:
        print(tokenname)
        return
    with open(filename, encoding='utf-8') as data:
        raw_string = data.readline()
        split_string = '{\"rightsize'
        string_list = [split_string + s[:-2] for s in raw_string.split(split_string) if len(s) >= 2]
        for string_dict in string_list:
            try:
                result_dict = ast.literal_eval(string_dict)
            except SyntaxError:
                result_dict = ast.literal_eval(string_dict + '}')
            left_str = [ldict['str'].split(' ') for ldict in result_dict['Left']]
            left_str = [string for sublist in left_str for string in sublist]
            left_str = ' '.join(left_str)
            right_str = [rdict['str'].split(' ') for rdict in result_dict['Right']]
            right_str = [string for sublist in right_str for string in sublist]
            right_str = ' '.join(right_str)
            query = '''INSERT INTO {0} VALUES ('{1}','{2}','{3}')'''.format(tokenname, result_dict['Kwic'][0]['str'], left_str.replace("\'", "\'\'"), right_str.replace("\'", "\'\'"))
            try:
                c.execute(query)
            except sqlite3.OperationalError:
                print(query)
    conn.commit()
    print(tokenname)

for file in os.listdir(datadir):
    filename = os.fsdecode(file)
    tokenname = filename[0:-8]
    process_raw_json(datapath+filename, tokenname, conn)

conn.close()