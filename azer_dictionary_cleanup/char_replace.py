char_dict = {
    "À": "A",
    "à": "a",
    "Á": "B",
    "á": "b",
    "Ú": "C",
    "ú": "c",
    "×": "Ç",
    "÷": "ç",
    "Ä": "D",
    "ä": "d",
    "Å": "E",
    "å": "e",
    "ß": "Ə",
    "ÿ": "ə",
    "Ô": "F",
    "ô": "f",
    "Ý": "G",
    "ý": "g",
    "Ü": "Ğ",
    "ü": "ğ",
    "Ù": "H",
    "ù": "h",
    "Õ": "X",
    "õ": "x",
    "Û": "I",
    "û": "ı",
    "È": "İ",
    "è": "i",
    "Æ": "J",
    "æ": "j",
    "Ê": "K",
    "ê": "k",
    "Ã": "Q",
    "ã": "q",
    "Ë": "L",
    "ë": "l",
    "Ì": "M",
    "ì": "m",
    "Í": "N",
    "í": "n",
    "Î": "O",
    "î": "o",
    "Þ": "Ö",
    "þ": "ö",
    "Ï": "P",
    "ï": "p",
    "Ð": "R",
    "ð": "r",
    "Ñ": "S",
    "ñ": "s",
    "Ø": "Ş",
    "ø": "ş",
    "Ò": "T",
    "ò": "t",
    "Ó": "U",
    "ó": "u",
    "Ö": "Ü",
    "ö": "ü",
    "Â": "V",
    "â": "v",
    "É": "Y",
    "é": "y",
    "Ç": "Z",
    "ç": "z"
}

with open("in.txt", encoding="utf-8") as infile, open ("out.txt", mode="w", encoding="utf-8") as outfile:
    for line in infile:
        for char in line:
            try:
                out_char = char_dict[char]
                outfile.write(out_char)
            except KeyError:
                outfile.write(char)    