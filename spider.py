import sys
import datetime
import sqlite3
import pdb
import urllib.request
from bs4 import BeautifulSoup

from text import parse_text, parse_links

''' Web crawler that searches for a key word within the pages it crawls.
    if keyword is found it updates the entry in the database.
'''

class dbPages(object):
    def connect(self):
        self.conn = sqlite3.connect('db.sqlite')
        self.cur = self.conn.cursor()
        # keyword: T/F if keyword exists, date: date of crawl, error: store error
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Pages
            (id INTEGER PRIMARY KEY, url TEXT UNIQUE,
            date TEXT, error TEXT, crawled INTEGER)''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Words
            (id INTEGER PRIMARY KEY, word TEXT UNIQUE,
             count INTEGER )''')
        self.conn.commit()



        self.conn.commit()

    #create new entry
    def create_url(self, url):
        self.cur.execute('INSERT OR IGNORE INTO Pages (url) VALUES ( ? )', (url,))
        self.conn.commit()

    #get next url to crawl
    def get_next_url(self):
        self.cur.execute('SELECT url FROM Pages WHERE crawled is NULL ORDER BY ID ASC LIMIT 1')
        row = self.cur.fetchone()
        return row

    #get specific entry
    def get_url(self, url):
        return self.cur.execute('SELECT id, url FROM Pages WHERE url=?', (url,))
        row = self.cur.fetchone()
        return row

    #update existing entry
    def update_url(self, page):
        self.cur.execute('UPDATE Pages SET crawled=?, date=?, error=? WHERE url=?',
                    (page.crawled, page.date, page.error, page.url))
        self.conn.commit()

    def create_or_update_word(self, word_info):
        self.cur.execute('INSERT OR IGNORE INTO Words (word, count) VALUES( ?, ?)', (word_info.word, word_info.count))
        #TODO - this will reincrement if we create the word and then update it.
        self.cur.execute('UPDATE Words SET count=count+? WHERE word=?', (word_info.count, word_info.word))
        self.conn.commit()

class pageMagic(object):
    def __init__(self, url):
        self.url = url
        self.crawled = 0
        self.date = datetime.datetime.now()
        self.error = None

    def __repr__(self):
        return {'url': self.url, 'error': self.error,
                'date': self.date, 'crawled': self.crawled}

    def fetchHTML(self):
        try:
            with urllib.request.urlopen(self.url) as response:
                self.html = response.read()
            self.crawled = 1
        #http error etc. ex <urlopen error [Errno 8] nodename nor servname provided, or not known>
        except urllib.error.URLError as e:
            #to do- write error to db
            self.error = str(e)
        except ValueError as e:
            self.error = str(e)


    def wordCount(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        x = parse_text(self.soup)


    def getLinks(self):
        a = self.soup.find_all('a')
        links = parse_links(a, self.url)


def spider(start_url, max_tries):
    test = True
    counter = 0
    #initialize db
    db = dbPages()
    db.connect()

    #create first entry
    db.create_url(start_url)

    while counter <= int(max_tries):
        #get the next url that hasn't been crawled
        row = db.get_next_url()

        #start crawl
        page = pageMagic(row[0])
        page.fetchHTML()
        #if we can access the html, search for our keyword and links
        if not page.error:
            page.topHundred()

            #get links on page
            links = page.getLinks()
            for link in links:
                #write to db for future spidering
                db.create_url(link)

        #update with page info we found
        db.update_url(page)
        counter = counter + 1

    print (str(max_tries) + ' urls attempted!')

spider(sys.argv[1], sys.argv[2])

#python spider.py "https://www.hillaryclinton.com" 100

