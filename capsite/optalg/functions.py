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


def get_alg_page(wiki_url):
	content = get_page(wiki_url)

	soup = bs(content)

	title_tag = soup.find('title')
	name = title_tag.string

	p_tags = soup.findAll('p')
	desc = p_tags[0].string

	return name, desc, wiki_url



class AlgNode:
	def __init__(self, id, name, description, wiki_url):
		#int
		self.id = id
		#str
		self.name = name
		#str
		self.description = description
		#str
		self.wiki_url = wiki_url
		#lst
		self.related_algs = []
		#dictionary
		self.related_alg_count = {}

		#future variables to incorporate
		#avg_date_used =
		#category = 
	
	#necessary function for the add_related_alg func
	def related_algs_sort_key(self, node):
		#include other factors later on such avg_date_algorithm is implemented
		return self.related_alg_count[node.id]

	def add_related_algs(self, related_algs):
		#add possible related algorithms
		for alg in related_algs:
			if alg in self.related_algs:
				self.related_alg_count[alg.id] = self.related_alg_count[alg.id] + 1
			else:
				self.related_algs.append(alg)
				self.related_alg_count[alg.id] = 1

		#reorganize into most related algorithm based on the count
		self.related_algs.sort(key=self.related_algs_sort_key, reverse=True)


	def return_related_algs(self):
		return self.related_algs



#def get_new_id():


#needs to be updated to method with static storage
algnodes_lst = []


#horrendous complexity that needs to be updated
def update_related_algs(wiki_urls):
	related_algs = []

	#creates new algnode objects if not existant yet
	for url in wiki_urls:
		name, desc, _ = get_alg_page(url)

		alg_node_exists = False
		for alg_node in algnodes_lst:
			if alg_node.name == name:
				alg_node_exists = True
				related_algs.append(alg_node.related_algs)

		if not alg_node_exists:
			new_alg = AlgNode(get_new_id(),name,desc,url)
			algnodes_lst.append(new_alg)
			related_algs.append(new_alg)

	#add number of connections to alg nodes
	for alg_node in related_algs:
		alg_node.add_related_algs(related_algs)


def get_related_algs(wiki_urls):
	curr_algs = []
	related_algs = []

	for url in wiki_urls:
		for alg_node in algnodes_lst:
			if alg_node.wiki_url == url:
				curr_algs.append(alg_node)

	for alg_node in curr_algs:
		related_algs.append(alg_node.return_related_algs())

	return related_algs