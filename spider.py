import argparse
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

''' Web crawler that searches for a key word within the pages it crawls.
    if keyword is found it updates the entry in the database.
'''

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Pages
    (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, html TEXT,
     keyword INTEGER, date TEXT)''')

class pageMagic(object):
    def __init__(self, url):
        self.url = url

    def fetchHTML(self):
        with urllib.request.urlopen(self.url) as response:
            self.html = response.read()
            return self.html

    def keywordSearch(self, keyword):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        if keyword in self.soup.get_text():
            print (keyword + ' found!')
            self.keyword = True
            return self.keyword
            #TODO: update db entry with keyword search results

    def getLinks(self):
        links = []
        for item in self.soup.find_all('a'):
            link = item.get('href')
            if not link:
                continue
            else:
                links.append(link)
        # TODO: write to db
        #print (links)

def spider(start_url, keyword, max_urls):
    #TODO: start crawl, continue with next entry in the db
    page = pageMagic(start_url)
    page.fetchHTML()
    page.keywordSearch(keyword)
    page.getLinks()


spider("http://isthelakefullyet.com/", "Lake", 10)