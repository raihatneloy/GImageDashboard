import urllib
import mechanize
import json
from bs4 import BeautifulSoup
from urlparse import urlparse

url = 'https://www.google.com/search?source=lnms&tbm=isch&q='

def getPic (search):
	try:
		browser = mechanize.Browser()
		browser.set_handle_robots(False)
		browser.addheaders = [('User-agent','Mozilla')]

		htmlText = browser.open(url + search)

		img_url = []

		soup = BeautifulSoup(htmlText, 'html.parser')
		divs = soup.find_all(divs)

		for div in divs:
			try:
				div_dict = json.loads(div.text)

				if div_dict.get('ou'):
					img_url.append({ 'main_url': div_dict['ou'], 'thumbnail_url': div_dict['tu'] })
			except:
				pass

		print img_url
	except:
		print "Can't get images! Server error!"

getPic('messi')