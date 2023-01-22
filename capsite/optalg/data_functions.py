from bs4 import BeautifulSoup as bs
import requests
import networkx as nx
import time
from optalg import models
from django.db.models import Q
import matplotlib.pyplot as plt
import random

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
			if models.Algorithm.objects.filter(url = str(alg_info[0])).exists():
				main_alg = models.Algorithm.objects.get(url=str(alg_info[0]))
				main_alg.scraped = True
				main_alg.save()
			else:
				main_alg = models.Algorithm.objects.create(url=str(alg_info[0]), scraped=True)

			#This list will be used to update the graph.
			related_nodes = []


			for datum in related_url_data:
				try:
					#for every new related algorithm detected in the scraped web page, we create a data entry in the db for the related algorithm to be queued for scraping.
					edge_alg, created = models.Algorithm.objects.get_or_create(name=str(datum[1]), desc=str(datum[2]), url=str(datum[0]))
					frontier_obj, _ = models.Frontier.objects.get_or_create(url=str(datum[0]))

					#add the related algorithm data into the list that will be used to update the graph
					related_nodes.append(edge_alg)
				except Exception as e:
					print(e)

			for node in related_nodes:
				try:
					#This is a bidirectional table which we represent without risk of duplicates is alg_one and alg_two are chosen by alphabetic order.
					if main_alg.url > node.url:
						edge, created = models.Edge.objects.get_or_create(alg_one=main_alg, alg_two=node)
					else:
						edge, created = models.Edge.objects.get_or_create(alg_one=node, alg_two=main_alg)
					#If its a new edge it has a weight of 1, otherwise we increase weight by 1
					if created:
						edge.save()
					else:
						edge.weight = edge.weight + 1
						edge.save()
				except Exception as e:
					print(e)

		except Exception as e:
			print(e)

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
		except Exception as e:
			print(e)


#This function is used to create an image of the algorithm network using the networkx library.
def create_graph(edge_query):
	#We construct the network in networkX
	g = nx.Graph()
	for edge in edge_query:
		g.add_edge(edge.alg_one, edge.alg_two, weight=edge.weight)
	
	#We draw the network
	nx.draw(g, with_labels = True)
	#We select a random number to assign as a name to the image.
	pic_id = random.randint(10000,99999)
	#We save the image and return the picture id so we can display it to the user. 
	plt.savefig("/optalg/static/optalg/network_imgs/{}.png".format(pic_id))
	plt.close()
	
	return pic_id


#This function gets the related algorithms from the saved network graph and returns it as a list.
def return_related_algs(url):
	#get the algorithm data object
	try:
		main_alg = models.Algorithm.objects.get(url=url)
	except:
		return [], None
	#Query the top 10 edges ordered by weight
	edge_query = models.Edge.objects.filter(Q(alg_one=main_alg) | Q(alg_two=main_alg)).order_by('-weight')[:10]
	#Get related algorithm information from the edges
	related_algs = []
	for edge in edge_query:
		if edge.alg_one == main_alg:
			related_algs.append((edge.alg_one.name, edge.alg_one.desc, edge.alg_one.url))
		else:
			related_algs.append((edge.alg_two.name, edge.alg_two.desc, edge.alg_two.url))

	#We create a picture of the graph to show on the frontend and return the picture name. 
	pic_id = create_graph(edge_query)

	return related_algs, pic_id