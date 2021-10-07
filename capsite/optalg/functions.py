from bs4 import BeautifulSoup as bs
import requests

def get_page(link):
	url = link
	if "http" or "https" not in url:
		url = "http://" + url

	req = requests.get(url)
	content = req.text

	return content

def get_all_links(content):
	soup = bs(content)

	a_tags = soup.findAll('a')
	urls = [a.get('href') for a in a_tags]
	urls = [l for l in urls if l is not None]


	wiki_links = [l for l in urls if "wiki" in l]
	wiki_links = ["https://en.wikipedia.org" + l for l in wiki_links if ".org" not in l]

	processed_links = [l for l in wiki_links if "algo" in l]

	return processed_links