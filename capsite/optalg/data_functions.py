from bs4 import BeautifulSoup as bs
import requests
import networkx as nx
import time
from optalg import models

#Purpose: To get the algorithm name, description, and a list of related algorithms from provided algorithm wikipedia page. 
class WebScraper:
	#The methods of this class all work in tandem when called by the run() method. The default option is to run the run() method upon initialization. 
	def __init__(self, url=None, run=True):
		if run:
			self.run(url)
		else:
			pass

	#get_pages scrapes a web page for its content. 
	def get_page(self, link):
		url = link
		#standardizes url format
		if "http" not in url or "https" not in url:
			url = "http://" + url

		#requests web page and turns content into string form.
		req = requests.get(url)
		content = req.text

		#return the content of the web page.
		return content


	#finds and returns the wiki links for all algorithms in a wiki page
	def get_all_links(self, soup):
		#first we find all hyperlink tags (<a>)
		a_tags = soup.findAll('a')
		#get the actual hyperlink values. When one is not present, the current method provides a None value instead. We remove None values. 
		urls = [a.get('href') for a in a_tags]
		urls = [l for l in urls if l is not None]


		#We use wikipedia as our data source because it helps standardize data collection.
		#Here we filter for hyperlinks from wikipedia. 
		wiki_links = [l for l in urls if "wiki" in l]
		wiki_links = [l for l in wiki_links if "google" not in l]
		#Here we format for wikipedia links to match how we will use them
		wiki_links = ["https://en.wikipedia.org" + l for l in wiki_links if ".org" not in l]

		#Here we filter for hyperlinks that have to do with algorithms
		processed_links = [l for l in wiki_links if "algo" in l]

		return processed_links


	#gets the basic information of an algorithm from a wiki url
	def get_alg_info(self, wiki_url):
		#call the method that requests the wikipedia page and returns its content
		content = self.get_page(wiki_url)

		#format the wikipedia page content into BeautifulSoup format
		soup = bs(content)

		#Get the title of the wikipedia page
		title_tag = soup.find('title')
		name = title_tag.string

		#Get the text content of the wikipedia page found by the paragraph tag <p> from html
		#Then select the first paragraph which is usually the description. 
		p_tags = soup.findAll('p')
		desc = p_tags[0].string

		#calls the get_all_links method which finds all related algorithm links from the wikipedia page. 
		related_urls = self.get_all_links(soup)

		return name, desc, related_urls


	#Our data is stored in a connected network graph. This method updates the graph to account for the data collection from the newly scraped algorithm wikipedia page. 
	def update_graph(self, alg_info, related_url_data):
		#This function is vital to the functioning of the web app in that it can fail but it cannot return an error. To combat this, a try statement is used. 
		try:
			#The frontier database's main function is provide a database for us to account for which algorithms have already been scraped to prevent duplicates if they have
			#and to queue them for scraping if they have not. 
			#This if statement checks if a algorithm is already in our db and marks it as scraped (searched), else it inserts an entry marked as scraped.
			if models.Frontier.objects.filter(url = str(alg_info[0])).exists():
				alg_obj = models.Frontier.objects.get(url=str(alg_info[0]))
				alg_obj.searched = True
				alg_obj.save()
			else:
				alg_obj = models.Frontier(url=str(alg_info[0]), searched=True)
				alg_obj.save()
			

			#Read the graph data and open it in the object G.
			G = nx.read_gexf("graph_data")

			#This list will be used to update the graph.
			related_nodes = []


			for datum in related_url_data:
				#sleep inserted to provide server processor a "break" since this algorithm is running constantly in the background and time.
				time.sleep(1)
				#for every new related algorithm detected in the scraped web page, we create a data entry in the db for the related algorithm to be queued for scraping.
				alg_obj, created = models.Frontier.objects.get_or_create(url=str(datum[0]))

				#add the related algorithm data into the list that will be used to update the graph
				related_nodes.append((str(datum[1]), str(datum[2]), str(datum[0])))

			#Create a node if it doesn't exist containing the algorithm name, description, and url in that order.
			G.add_node(url, name=str(alg_info[1]), desc=str(alg_info[2]), url=str(alg_info[0]))

			for node in related_nodes:
				#Create a node if it doesn't exist for all related algorithms
				G.add_node(str(node[2]), name=str(node[0]), desc=str(node[1]), url=str(node[2]))
				#If an edge exists between the main algorithm node and the related algorithm node, increase its weight by 1, otherwise, create an edge between the two.
				try:
					G[str(url)][str(node[2])][weight] = G[str(alg_info[0])][str(node[2])][weight] + 1
				except:
					G.add_edge(str(alg_info[0]), str(node[2]), weight=1)
			#save the data by writing the graph back into the file. 
			nx.write_gexf(G, "graph_data")
		except:
			pass

	#This method runs the all the above method for the purpose of taking a url of a wikipedia algorithm page, scraping it, and updating our database and graph.
	def run(self, url):
		try:
			#get the name, description, and related urls of the of the provided algorithm url
			name, desc, related_urls = self.get_alg_info(url)
			alg_info = (url, name, desc, related_urls)

			#get the algorithm information for all related algorithms found from the main algorithm's wikipedia page. 
			related_url_data = []
			for related_url in related_urls:
				#sleep inserted to provide wikipedia servers a "break" from our requests and to prevent us from being flagged as a bot and blocked. 
				time.sleep(1)
				related_name, related_desc, _ = self.get_alg_info(str(related_url))
				related_url_data.append((related_url, related_name, related_desc))

			#update the data
			self.update_graph(alg_info, related_url_data)
		except:
			pass


#This function gets the related algorithms from the saved network graph and returns it as a list.
def return_related_algs(url):
	#read the graph network file
	G = nx.read_gexf("graph_data")
	#Find the all nodes connected to the requested algorithm sorted by edge weight which represents similarity of algorithms.
	related_algs = sorted(G[url].items(), key=lambda edge: edge[1]['weight'],reverse=True)
	#Get the top 10 related algorithms.
	related_algs = related_algs[:10]
	#Get algorithm information from the nodes
	related_algs = [alg[0] for alg in related_algs]
	return related_algs