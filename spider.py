import sys

from models import pageMagic, dbPages
from text import parse_text, parse_links

''' Web crawler that searches for a key word within the pages it crawls.
    if keyword is found it updates the entry in the database.
'''

def spider(start_url, max_tries):
    test = True
    counter = 1
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
            words = page.wordCount()
            for count, word in enumerate(words):
                if db.get_word(word):
                    db.update_word(word, count)
                    print ('updated ' + word)
                else:
                    db.create_word(word, count)
            # get links on page
            links = page.getLinks()
            for link in links:
                # write to db for future spidering
                db.create_url(link)

        #update with page info we found
        db.update_url(page)
        counter = counter + 1
        print (counter)

    print (str(max_tries) + ' urls attempted!')

spider(sys.argv[1], sys.argv[2])

#python spider.py "https://www.hillaryclinton.com" 100

