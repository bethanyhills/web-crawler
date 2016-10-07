# web-crawler
Web crawler that spiders URLs for a given domain, parses HTML for text and links, records words & frequency. The data is then be queried and manipulated for use in data visualizations.

Uses python, sqlite, beautiful soup, urllib, enchant, textblob

#To run:
1. Confirm you have sqlite installed
2. Clone this repo
3. Install the requirements
4. from the command line, run the program with your desired parameters (starting URL, # of URLs to spider for this domain). 
  Ex. python spider.py "https://www.hillaryclinton.com" 100
  
#Live:
This web crawler was used to power a D3 word cloud of the most frequent words on each of the 2016 presidential candidate websites: http://www.potentialprezsays.com/

