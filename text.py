from collections import Counter
import enchant
from numpy import interp
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
            if len(word) > 3 and len(word) < 25:
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
        if ';' in link:
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

def map_to_range(rows):
    max = 0
    min = 1000
    for row in rows:
        if row[1] > max:
            max = row[1]
        if row[1] < min:
            min = row[1]
    return [min, max]

#write data to js file
def to_js(rows):
    range = map_to_range(rows)

    print('writing file')
    writer = open('words_trump.js', 'w')
    writer.write("words_trump = [")
    first = True
    for row in rows:
        if not first: writer.write(",\n")
        first = False
        word = row[0]
        count = round(interp(row[1], [range[0], range[1]], [0, 40]))
        #count = round(row[1] / 100)
        writer.write("{text: '" + word + "', size: " + str(count) + "}")
    writer.write("\n];\n")
    writer.close()
