import sqlite3
import urllib.request
from bs4 import BeautifulSoup

'''Web crawler that searches for a key word and if found adds the URL to the database'''

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()

def fetchHTML(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        return html


def keywordSearch(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    if keyword in soup.get_text():
        print (keyword + ' found!')
        return True

page = fetchHTML("http://isthelakefullyet.com/")
keywordSearch(page, 'Lake')


# def spider(url, word):
#     soup = BeautifulSoup()
#     #search page