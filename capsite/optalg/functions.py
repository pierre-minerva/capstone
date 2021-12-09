from bs4 import BeautifulSoup as bs
import requests
import networkx as nx
import time
from optalg import models

#scrapes a web page
def get_page(link):
	url = link
	if "http" not in url or "https" not in url:
		url = "http://" + url

	req = requests.get(url)
	content = req.text

	return content


#finds and returns the wiki links for all algorithms in a wiki page
def get_all_links(soup):
	a_tags = soup.findAll('a')
	urls = [a.get('href') for a in a_tags]
	urls = [l for l in urls if l is not None]


	wiki_links = [l for l in urls if "wiki" in l]
	wiki_links = [l for l in wiki_links if "google" not in l]
	wiki_links = ["https://en.wikipedia.org" + l for l in wiki_links if ".org" not in l]

	processed_links = [l for l in wiki_links if "algo" in l]

	return processed_links


#gets the basic information of an algorithm from a wiki url
def get_alg_info(wiki_url):
	content = get_page(wiki_url)

	soup = bs(content)

	title_tag = soup.find('title')
	name = title_tag.string

	p_tags = soup.findAll('p')
	desc = p_tags[0].string

	related_urls = get_all_links(soup)

	return name, desc, related_urls


def update_graph(url):
	try:
		if models.Frontier.objects.filter(url = str(url)).exists():
			alg_obj = models.Frontier.objects.get(url=str(url))
			alg_obj.searched = True
			alg_obj.save()
		else:
			alg_obj = models.Frontier(url=str(url), searched=True)
			alg_obj.save()

		time.sleep(1)
		name, desc, related_urls = get_alg_info(url)

		G = nx.read_gexf("graph_data")

		frontier = []
		related_nodes = []

		for related_url in related_urls:
			time.sleep(1)
			related_name, related_desc, _ = get_alg_info(str(related_url))
			alg_obj, created = models.Frontier.objects.get_or_create(url=str(related_url))

			related_nodes.append((str(related_name), str(related_desc), str(related_url)))

		G.add_node(url, name=str(name), desc=str(desc), url=str(url))

		for node in related_nodes:
			G.add_node(str(node[2]), name=str(node[0]), desc=str(node[1]), url=str(node[2]))
			try:
				G[str(url)][str(node[2])][weight] = G[str(url)][str(node[2])][weight] + 1
			except:
				G.add_edge(str(url), str(node[2]), weight=1)
		nx.write_gexf(G, "graph_data")
	except:
		pass

def return_related_algs(url):
	G = nx.read_gexf("graph_data")
	related_algs = sorted(G[url].items(), key=lambda edge: edge[1]['weight'],reverse=True)
	related_algs = related_algs[:10]
	print(related_algs)
	related_algs = [alg[0] for alg in related_algs]
	print(related_algs)
	return related_algs