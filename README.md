# web-crawler
Web crawler that spiders URLs for a given domain, parses HTML, records words & frequency, and visualizes it in D3 for a given domain.

Uses python, sqlite, beautiful soup, urllib, enchant, textblob

#To run:
1. Confirm you have sqlite installed
2. Clone this repo
3. Install the requirements
4. from the command line, run the program with your desired parameters (starting URL, # of URLs to spider for this domain). 
  Ex. python spider.py "https://www.hillaryclinton.com" 100
  
#Goal:
Use D3 to visualize this data for the domain of each presidential candidate.
