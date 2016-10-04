from collections import Counter
import enchant
import re

def parse_text(soup_text):
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
    for item in link_text:
        link = item.get('href')
        if not link:
            continue
        substring = ['http', 'https', 'www']
        if not any(x in link for x in substring):
            # valid link, do nothing
            pass
        else:
            # create full domain by appending subdomain. ex. 'http://www.hillaryclinton.com' + '/issues'
            if self.url.endswith('/'):
                link = self.url[:-1] + link
            else:
                link = self.url + link
        if check_domain(domain, link):
            links.append(link)
    return links

#limit our spidering to specific domain
def check_domain(domain, link):
    if domain in link:
        return True
    else:
        return False