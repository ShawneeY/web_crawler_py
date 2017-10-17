from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.domain.com.au/auction-results/melbourne/'

# opening connection and download the page
uClient = uReq(my_url)

# offload content to a var
page_html = uClient.read()

# close  connection
uClient.close()

# HTML parsing
page_soup = soup(page_html, "html.parser")

# grab auction details
auction_details = page_soup.findAll("a", {"class","auction-details"})

print(page_soup.h1)