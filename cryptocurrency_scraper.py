
"""
    Filename: cryptocurrency_scraper.py
    Author: Jeff Gladstone
    Date: January, 2018
    Description:
    This program parses HTML from the CoinMarketCap home web page
    to create and display a list of cryptocurrencies with name, price and price change.
    It also writes XML to an output document called 'currencies.xml'
"""


# Initial imports
from lxml import html
import requests
import datetime

# The headers line prevents the 403 error on the request --- some websites have security that requires this header
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get('https://coinmarketcap.com/', headers=headers)
tree = html.fromstring(page.content)

# Parse HTML
names = tree.xpath('//table[@id="currencies"]//a[@class="currency-name-container"]/text()')
prices = tree.xpath('//table[@id="currencies"]//a[@class="price"]/text()')
changes = tree.xpath('//table[@id="currencies"]//td/text()')
changes = list(filter(lambda k: ' ' not in k, changes))

# Combine the three lists into one list of tuples. Tuple contains name, price and price change of currency
currencies = list(zip(names, prices, changes))

# Write to output document
with open("currencies.xml", "w") as f:
	for currency in currencies:
		f.write("<currency>\n")
		f.write("\t<name>" + currency[0] + "</name>\n")
		f.write("\t<price>" + currency[1] + "</price>\n")
		f.write("\t<change>" + currency[2] + "</change>\n")
		f.write("</currency>\n")

# Initialize variable for today's date and time
now = datetime.datetime.now()
now = now.strftime("%A, %B %d, %Y at %I:%M %p")

# Display currency name, price and price change
print("\nCryptocurrency information for " + now + ':\n')
for currency in currencies:
		print(currency[0] + ' - ' + currency[1] + ' [' + currency[2] + ']')