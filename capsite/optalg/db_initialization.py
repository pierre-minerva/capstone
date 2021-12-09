from optalg import functions
from background_task import background
from optalg import models
import time
import networkx as nx

wiki_algs_list = "https://en.wikipedia.org/wiki/List_of_algorithms"
_, _, init_algs = functions.get_alg_info(wiki_algs_list)

G = nx.Graph()
nx.write_gexf(G, "graph_data")

for alg_url in init_algs:
	try:
		functions.update_graph(alg_url)
	except:
		pass