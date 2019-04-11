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
            word["suggestions"] = v.suggest(word["value"])
            errors.append(word)
    v.terminate()
    return errors

def cliOutput(errorDictionaries, printSuggestions=True, onlywithSuggestions=False):
    for word in errorDictionaries:
        if onlywithSuggestions and len(word["suggestions"]) == 0:
            continue
        if(printSuggestions):
            print(str(word["linenumber"]) + " error: " + word["value"] + " suggestions: " + str(word["suggestions"]))
        else:
            print(str(word["linenumber"]) + " error: " + word["value"])




if __name__ == "__main__":
    filename = sys.argv[1]
    misspellings = analyzeWords(readWords(filename))
    print("---------\n------\n---")
    printSugs = "-s" in sys.argv
    onlySugs = "-o"  in sys.argv
    cliOutput(misspellings, printSuggestions=printSugs, onlywithSuggestions=onlySugs)

