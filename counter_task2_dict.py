import json

EXCLUDE_LEFT = ['məli', 'malı', 'mək', 'maq']
DAT_CASE = ['a', 'ə']
ACC_CASE = ['i', 'u', 'ü', 'ı']
EXCLUDE_PREV_WORD = ['in', 'un', 'ün', 'ın']
END_OF_SENTENCE = ['.', '?', '!', '\n']

with open('dict_entries.txt', encoding='utf-8') as f:
    DICT_ENTRIES = set([string[:-1] for string in f.readlines()])

with open('data/task1.json') as f:
    json_data = json.load(f)
    tokens = list(json_data.keys())

pruned_dict_entries = open('pruned_dict_entries.txt', encoding='utf-8', mode='w')
all_results_pruned = open('all_results_pruned.txt', encoding='utf-8', mode='w')
no_results_found = open('no_results_found.txt', encoding='utf-8', mode='w')

def EOS_prune(word_list, kept_words, position):
    if position == len(word_list) - 1:
        return word_list
    elif word_list[position] in END_OF_SENTENCE:
        return kept_words
    else:
        kept_words.append(word_list[position])
        return EOS_prune(word_list, kept_words, position+1)

def pull_cased_nouns(word_list, case_markers, position, pulled_words):
    if position >= len(word_list) - 1:
        return pulled_words
    curr_word = word_list[position]
    if len(curr_word) >= 2 and curr_word[-1] in case_markers:
        if curr_word.upper() in DICT_ENTRIES:
            pruned_dict_entries.write(word + '\t\t\t\t\t' + curr_word + '\n')
            return pull_cased_nouns(word_list, case_markers, position+1, pulled_words)
        if curr_word[-2] == 'n':
            if position >= 1 and word_list[position-1][-2:] in EXCLUDE_PREV_WORD:
                return pull_cased_nouns(word_list, case_markers, position+1, pulled_words)
            elif position == 0:
                return pull_cased_nouns(word_list, case_markers, position+1, pulled_words)
        pulled_words.append(curr_word)
    return pull_cased_nouns(word_list, case_markers, position+1, pulled_words)

results_dat = dict()
results_acc = dict()

for token in tokens:
    try:
        token_lines = json_data[token]['Lines']
    except KeyError:
        no_results_found.write(token + '\n')
        continue
    
    token_dat_results = dict()
    token_acc_results = dict()

    for line in token_lines:
        try:
            word = line['Kwic'][0]['str']
            if word.endswith(token):
                #exclude word-final appearance
                continue
            left = [ldict['str'].split(' ') for ldict in line['Left']]
            left = [string for sublist in left for string in sublist]
            for left_word in left:
                if any(x in left_word for x in EXCLUDE_LEFT):
                    #exclude specific left-occuring words
                    raise ValueError
            left.reverse()            
            right = [rdict['str'].split(' ') for rdict in line['Right']]
            right = [string for sublist in right for string in sublist]

            #remove words outside of sentence
            left = EOS_prune(left, [], 0)
            left.reverse()
            right = EOS_prune(right, [], 0)

            pulled_dat_list = pull_cased_nouns(left, DAT_CASE, 0, []) + pull_cased_nouns(right, DAT_CASE, 0, [])
            pulled_acc_list = pull_cased_nouns(left, ACC_CASE, 0, []) + pull_cased_nouns(right, ACC_CASE, 0, [])

            curr_dat_results = token_dat_results.get(word, {})
            curr_acc_results = token_acc_results.get(word, {})

            for pulled_dat in pulled_dat_list:
                curr_dat_results[pulled_dat] = curr_dat_results.get(pulled_dat, 0) + 1
            token_dat_results[word] = curr_dat_results

            for pulled_acc in pulled_acc_list:
                curr_acc_results[pulled_acc] = curr_acc_results.get(pulled_acc, 0) + 1
            token_acc_results[word] = curr_acc_results

        except ValueError:
            continue

    results_dat[token] = token_dat_results
    results_acc[token] = token_acc_results

#    if not results_dat:
#        all_results_pruned.write(token + '\n')
"""
for token in results_dat:
    results_dat[token] = sorted(results_dat[token], key=results_dat[token].get, reverse=True)

for token in results_acc:
    results_acc[token] = sorted(results_acc[token], key=results_acc[token].get, reverse=True)
"""
with open('data/dative_pruned.json', mode='w') as f:
    json.dump(results_dat, f)

with open('data/accusative_pruned.json', mode='w') as f:
    json.dump(results_acc, f)

pruned_dict_entries.close()
all_results_pruned.close()
no_results_found.close()