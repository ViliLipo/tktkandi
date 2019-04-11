import libvoikko
import sys
import re
import string

def removeTexCommandsFromLine(line):
    line = re.sub('\\\\[\w[]*]*\*?(\{[\w -_:]*\})*', ' ', line)
    return line

def removePunctuationFromWord(word):
    word = re.sub('[.,]', '', word)
    return word

def handleSpecialCharacters(line):
    words = []
    line = removeTexCommandsFromLine(line)
    for word in line.split():
        for word2 in word.split("~"):
            words.append(removePunctuationFromWord(word2)) 
    return words


def readWords( filename):
    f = open(filename, "r", encoding="utf-8")
    lines = f.readlines()
    words = []
    linenumber = 0
    for line in lines:
        linenumber = linenumber + 1
        for word in handleSpecialCharacters(line):
            data = {'value': word, 'linenumber': linenumber}
            words.append(data)

    return words

def analyzeWords( words):
    v = libvoikko.Voikko(u"fi")
    errors = []
    for word in words:
        if not v.spell(word["value"]):
            errors.append("in line: " + str(word["linenumber"]) +" Error: " + str(word["value"] + " suggestion: " + str(v.suggest(word['value'])) ))
    v.terminate()
    return errors


if __name__ == "__main__":
    filename = sys.argv[1]
    misspellings = analyzeWords(readWords(filename))
    print("---------\n------\n---")
    for misspelling in misspellings:
        print(misspelling)

