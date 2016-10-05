import sqlite3
import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import datetime

from text import parse_text, parse_links

class dbPages(object):
    def connect(self):
        self.conn = sqlite3.connect('hillary2.sqlite')
        self.cur = self.conn.cursor()
        # keyword: T/F if keyword exists, date: date of crawl, error: store error
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Pages
            (id INTEGER PRIMARY KEY, url TEXT UNIQUE,
            date TEXT, error TEXT, crawled INTEGER)''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Words
            (id INTEGER PRIMARY KEY, word TEXT UNIQUE,
             count INTEGER )''')
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
    #create word and count
    def create_word(self, word, count):
        self.cur.execute('INSERT OR IGNORE INTO Words (word, count) VALUES( ?, ?)', (word, count))
        self.conn.commit()
    #increment count
    def update_word(self, word, count):
        self.cur.execute('UPDATE Words SET count=count+? WHERE word=?', (count, word))
        self.conn.commit()

    def get_word(self, word):
        self.cur.execute('SELECT id, word FROM Words WHERE word=?', (word, ))
        row = self.cur.fetchone()
        return row

    def get_top_words(self):
        self.cur.execute('SELECT word, count FROM Words ORDER BY count DESC LIMIT 100')
        rows = self.cur.fetchall()
        return rows

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
            req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'} )
            self.html = urlopen(req).read()
            # with urllib.request.urlopen(self.url) as response:
            #     self.html = response.read()
            self.crawled = 1
        #http error etc. ex <urlopen error [Errno 8] nodename nor servname provided, or not known>
        except urllib.error.URLError as e:
            #to do- write error to db
            self.error = str(e)
        except ValueError as e:
            self.error = str(e)


    def wordCount(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        words = parse_text(self.soup)
        return words


    def getLinks(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        a = self.soup.find_all('a')
        links = parse_links(a, self.url)
        return links