from requests import get
from bs4 import BeautifulSoup
import re
import json
import os

modes = ["preposition-after-verb", "preposition-after-adjective"]

def getlinksjson():
    def getlinks(mode, letter):
        soup = BeautifulSoup(
                    get(f"https://lingohelp.me/{mode}/{letter}").text,
                    "html.parser"
                    )
        tags = soup.find('main').find_all(
            'a', string=re.compile(".*more.*", flags=re.DOTALL)
            )
        links = []
        for a_elem in tags: links.append(a_elem['href'])
        res = {}
        for link in links:
            res[link.split('/')[2].split('-')[0] if link.split('/')[1]!="preposition-before-noun" else link.split('/')[2]] = 'lingohelp.me'+link
        return(res)

    letters = 'qwertyuiopasdfghjklzxcvbnm'
    for mode in modes:
        r = {}
        print(f"'{mode}' is copying...")
        for l in letters:
            r[l] = getlinks(mode, l)
        with open(f"{mode}.json", "w") as outfile: 
            json.dump(r, outfile)
        r = {}
getlinksjson()
print("Completed copying links")

for mode in modes:
    json = json.load(open(f'{mode}.json'))
    dirpath = mode.split('-')[-1]
    os.mkdir(dirpath)
    print(f"Copying HTMLs from {mode}")
    for links_with_letter in json:
        for name, link in json[links_with_letter].items():
            with open(f"{dirpath}/{name}.html", "w") as html:
                htmltext = get('https://'+link).text
                html.write(htmltext)
