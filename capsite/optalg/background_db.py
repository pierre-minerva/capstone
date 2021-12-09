from optalg import functions
from background_task import background
from optalg import models
import time
import networkx as nx

#A frontier based chronic update appraoch
@background(schedule=5)
def grow_db():
	new_alg_obj = models.Frontier.filter(searched=False)[0]
	functions.update_graph(new_alg_obj.url)

grow_db(repeat=5)
