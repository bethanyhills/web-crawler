import sqlite3
import urllib.request
from bs4 import BeautifulSoup

'''Web crawler that searches for a key word and if found adds the URL to the database'''

def fetchHTML(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        print (html)

fetchHTML("http://isthelakefullyet.com/")


# def spider(url, word):
#     soup = BeautifulSoup()
#     #search page