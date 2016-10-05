from collections import Counter
import enchant
import re

def parse_text(soup_text):
    print ('parsing text')
    strings = []
    d = enchant.Dict("en_US")
    for string in soup_text.stripped_strings:
        # remove all special characters
        new_string = re.sub('[^a-zA-Z0-9 \n\.]', '', string)
        # split into individual words
        words = new_string.split(' ')
        for word in words:
            #check this is a word in the english language
            if word:
                if d.check(word):
                    word = word.lower()
                    strings.append(word)
    # create a dictionary to count instances
    word_counts = Counter(strings)
    return word_counts

def parse_links(link_text, domain):
    print ('parsing links')
    links = []
    for item in link_text:
        link = item.get('href')
        if not link:
            continue
        #check full URLS
        substring = ['http', 'https', 'www']
        if any(x in link for x in substring):
            if check_domain(domain, link):
                links.append(link)
       #Format partial URLS
        else:
            #ex. 'http://www.hillaryclinton.com' + '/issues'
            if domain.endswith('/'):
                full_link = domain[:-1] + link
                links.append(full_link)
            else:
                full_link = domain + link
                links.append(full_link)
    return links

#limit our spidering to specific domain
def check_domain(domain, link):
    domain = domain.replace('https://', '')
    if domain in link:
        return True
    else:
        return False

#write data to js file
def to_js(rows):
    print('writing file')
    writer = open('words.js', 'w')
    writer.write("words = [")
    first = True
    for row in rows:
        if not first: writer.write(",\n")
        first = False
        word = row[0]
        count = row[1]
        writer.write("{word: '" + word + "', count: " + str(count) + "}")
    writer.write("\n];\n")
    writer.close()
