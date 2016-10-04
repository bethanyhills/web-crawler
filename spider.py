import argparse
import datetime
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

''' Web crawler that searches for a key word within the pages it crawls.
    if keyword is found it updates the entry in the database.
'''

class dbPages(object):
    def connect(self):
        self.conn = sqlite3.connect('db.sqlite')
        self.cur = self.conn.cursor()
        # keyword: T/F if keyword exists, date: date of crawl, error: store error
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Pages
            (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE,
             keyword INTEGER, date TEXT, error TEXT, crawled INTEGER)''')
        self.conn.commit()

    #create new entry
    def create(self, url):
        self.cur.execute('INSERT OR IGNORE INTO Pages (url) VALUES ( ? )', (url,))

        #cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', (url,))

        self.conn.commit()

    #get next url to crawl
    def get_next(self):
        self.cur.execute('SELECT url FROM Pages WHERE crawled is NULL ORDER BY ID ASC LIMIT 1')
        row = self.cur.fetchone()
        return row

    #get specific entry
    def get_entry(self, url):
        return self.cur.execute('SELECT id, url FROM Pages WHERE url=?', (url,))
        row = self.cur.fetchone()
        return row

    #update existing entry
    def update_entry(self, page):
        self.cur.execute('UPDATE Pages SET crawled=?, keyword=?, date=?, error=? WHERE url=?',
                    (page.crawled, page.keyword, page.date, page.error, page.url))
        self.conn.commit()

class pageMagic(object):
    def __init__(self, url):
        self.url = url
        self.keyword = 0
        self.crawled = 0
        self.date = datetime.datetime.now()
        self.error = None

    def __repr__(self):
        return {'url': self.url, 'keyword': self.keyword, 'error': self.error,
                'date': self.date, 'crawled': self.crawled}

    def fetchHTML(self):
        try:
            with urllib.request.urlopen(self.url) as response:
                self.html = response.read()
        #http error etc. ex <urlopen error [Errno 8] nodename nor servname provided, or not known>
        except urllib.error.URLError as e:
            #to do- write error to db
            self.error = e
            #print (e.data)

    def keywordSearch(self, keyword):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        if keyword in self.soup.get_text():
            print (keyword + ' found!')
            self.keyword = 1
            self.crawled = 1

    def getLinks(self):
        links = []
        for item in self.soup.find_all('a'):
            link = item.get('href')
            if not link:
                continue
            else:
                links.append(link)
        return links


def spider(start_url, keyword, max_urls):
    counter = 0
    #initialize db
    db = dbPages()
    db.connect()

    #create first entry
    db.create(start_url)

    while counter <= max_urls:
        #get the next url that hasn't been crawled
        row = db.get_next()
        print (row)

        #start crawl
        page = pageMagic(row[0])
        page.fetchHTML()
        #if we can access the html, search for our keyword and links
        if not page.error:
            page.keywordSearch(keyword)

            #get links on page
            links = page.getLinks()
            for link in links:
                #write to db for spidering
                db.create(link)

        #update with page info we found
        db.update_entry(page)
        counter = counter + 1

    print (str(max_urls) + ' crawled!')

#spider("http://isthelakefullyet.com/", "Lake", 2)