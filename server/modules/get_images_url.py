from bs4 import BeautifulSoup
import requests
import urllib2
import json

def get_soup(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), 'html.parser')

def get_images(query, max_images=100):
	global url

	image_type = "Action"
	print query
	query= query.split()
	query='+'.join(query)

	url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"

	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header)
	ActualImages=[]
	no_images = 0

	for a in soup.find_all("div",{"class":"rg_meta"}):
	    link , Type, thumbnail =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"], json.loads(a.text)["tu"]
	    ActualImages.append({"link": link, "type": Type, "thumbnail": thumbnail})

	    no_images = no_images + 1

	    if no_images == max_images:
	    	break
	
	return ActualImages