import string

with open("dict.txt", encoding="utf-8") as infile, open("dict_entries.txt", encoding="utf-8", mode="w") as outfile:
    for line in infile:
        try:
            word = line.split(maxsplit=1)[0]
            if word.isupper():
                word = word.strip(string.punctuation + string.digits + '´')
                if len(word) >= 2:
                    outfile.write(word + "\n")
        except IndexError:
            continue