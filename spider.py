import sys

from models import pageMagic, dbPages
from text import parse_text, parse_links, to_js

''' Web crawler that searches for a key word within the pages it crawls.
    if keyword is found it updates the entry in the database.
'''
def spider(start_url, max_tries):
    counter = 1

    #initialize db
    db = dbPages()
    db.connect()
    #create first entry
    db.create_url(start_url)

    #crawl the domain
    while counter <= int(max_tries):
        print ('spidering link number ' + str(counter))

        #get the next url that hasn't been crawled
        row = db.get_next_url()

        #start crawl
        page = pageMagic(row[0])
        print (page.url)
        page.fetchHTML()
        #if we can access the html, search for our keyword and links
        if not page.error:
            words = page.wordCount()
            print (len(words))
            for count, word in enumerate(words):
                if db.get_word(word):
                    db.update_word(word, count)
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

    #pull top words from db
    rows = db.get_top_words()
    #write them to a js file
    to_js(rows)




spider(sys.argv[1], sys.argv[2])

#python spider.py "https://www.hillaryclinton.com" 100

