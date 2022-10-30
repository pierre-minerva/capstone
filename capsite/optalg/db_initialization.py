from optalg import functions
from background_task import background
from optalg import models
import time
import networkx as nx

#This page is used to kickstart the database.  It contains a list of algorithms
wiki_algs_list = "https://en.wikipedia.org/wiki/List_of_algorithms"

#We create the network data file.
G = nx.Graph()
nx.write_gexf(G, "graph_data")
del G

#We run the Update class
Update = functions.WebScraper(url=wiki_algs_list, run=True)
del Update
