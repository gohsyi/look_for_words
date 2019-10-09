import re
from nltk.corpus import words
import urllib.request
from bs4 import BeautifulSoup


print(f"Currently there are {len(words.words())} words in our dictionary")
print("Looking for words that may exist?\n"
      "Try to type it below and use '_' to represent the word you are not sure about,\n"
      "'*' to represent any number of words (including none),\n"
      "'+' to represent any number of words (at least one word).")

verbose = input("\nDo you want to see words whose explaination cannot be found but are in our dictionary? (Y/N): ")
verbose = True if verbose == 'Y' or 'y' else False

print("\n[Example]\n"
      ">>> Please input your word: __st_ff")

WORDS = [chr(ord('a') + i) for i in range(26)]
ROOT_URL = 'http://www.iciba.com/'

while True:
    candidates = []
    word = input("\nPlease input your word ('q' to exist): ")
    word = word.lower()
    word = word.replace('_', '[a-z]')
    word = word.replace('*', '[a-z]*')
    word = word.replace('+', '[a-z]+')
    if word == 'q':
        break
    for w in words.words():
        match = re.match(word, w, flags=re.I)
        if match is not None and match.string == w:
            candidates.append(w)

    # print('You may want to search:', candidates)
    exists = []

    print('You may want to search:')

    for w in candidates:
        if verbose:
            print(f"\n[{w}]")
        url = ROOT_URL + w
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')
        tag_soup = soup.find(class_='base-list switch_part')
        if tag_soup is not None:
            if not verbose:
                print(f"\n[{w}]")
            meanings = tag_soup.find_all(class_='clearfix')
            for i in range(len(meanings)):
                translation = meanings[i].get_text()
                print(translation.replace('\n', ''))
            exists.append(w)

    if len(candidates) == 0:
        print("Sorry, we couldn't find any word according to your requirements.")
