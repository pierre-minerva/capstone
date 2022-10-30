from bs4 import BeautifulSoup as bs
import requests
import networkx as nx
import time
from optalg import models

class WebScraper:
	def __init__(self, url=None, run=True):
		if run:
			self.run(url)

	#scrapes a web page
	def get_page(self, link):
		url = link
		if "http" not in url or "https" not in url:
			url = "http://" + url

		req = requests.get(url)
		content = req.text

		return content


	#finds and returns the wiki links for all algorithms in a wiki page
	def get_all_links(self, soup):
		a_tags = soup.findAll('a')
		urls = [a.get('href') for a in a_tags]
		urls = [l for l in urls if l is not None]


		wiki_links = [l for l in urls if "wiki" in l]
		wiki_links = [l for l in wiki_links if "google" not in l]
		wiki_links = ["https://en.wikipedia.org" + l for l in wiki_links if ".org" not in l]

		processed_links = [l for l in wiki_links if "algo" in l]

		return processed_links


	#gets the basic information of an algorithm from a wiki url
	def get_alg_info(self, wiki_url):
		content = self.get_page(wiki_url)

		soup = bs(content)

		title_tag = soup.find('title')
		name = title_tag.string

		p_tags = soup.findAll('p')
		desc = p_tags[0].string

		related_urls = self.get_all_links(soup)

		return name, desc, related_urls


	def update_graph(self, alg_info, related_url_data):
		#This function is vital to the functioning of the web app in that it can fail but it cannot return an error. To combat this, a try statement is used. 
		try:
			if models.Frontier.objects.filter(url = str(alg_info[0])).exists():
				alg_obj = models.Frontier.objects.get(url=str(alg_info[0]))
				alg_obj.searched = True
				alg_obj.save()
			else:
				alg_obj = models.Frontier(url=str(alg_info[0]), searched=True)
				alg_obj.save()

			#sleep inserted to provide server processor a "break" since this algorithm is run constantly.
			time.sleep(1)
			

			G = nx.read_gexf("graph_data")

			related_nodes = []

			for datum in related_url_data:
				#sleep inserted to provide server processor a "break" since this algorithm is run constantly.
				time.sleep(1)
				alg_obj, created = models.Frontier.objects.get_or_create(url=str(datum[0]))

				related_nodes.append((str(datum[1]), str(datum[2]), str(datum[0])))

			G.add_node(url, name=str(alg_info[1]), desc=str(alg_info[2]), url=str(alg_info[0]))

			for node in related_nodes:
				G.add_node(str(node[2]), name=str(node[0]), desc=str(node[1]), url=str(node[2]))
				try:
					G[str(url)][str(node[2])][weight] = G[str(alg_info[0])][str(node[2])][weight] + 1
				except:
					G.add_edge(str(alg_info[0]), str(node[2]), weight=1)
			nx.write_gexf(G, "graph_data")
		except:
			pass

	def run(self, url):
		try:
			name, desc, related_urls = self.get_alg_info(url)
			alg_info = (url, name, desc, related_urls)

			related_url_data = []
			for related_url in related_urls:
				time.sleep(1)
				related_name, related_desc, _ = self.get_alg_info(str(related_url))
				related_url_data.append((related_url, related_name, related_desc))

			self.update_graph(alg_info, related_url_data)



def return_related_algs(url):
	G = nx.read_gexf("graph_data")
	related_algs = sorted(G[url].items(), key=lambda edge: edge[1]['weight'],reverse=True)
	related_algs = related_algs[:10]
	print(related_algs)
	related_algs = [alg[0] for alg in related_algs]
	print(related_algs)
	return related_algs