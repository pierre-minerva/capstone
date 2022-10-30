from optalg import functions
from background_task import background
from optalg import models
import time
import networkx as nx

#A frontier based chronic update appraoch
@background(schedule=10)
def grow_db():
	new_alg_obj = models.Frontier.filter(searched=False)[0]
	Update = functions.WebScraper(url=new_alg_obj.url, run=True)
	del Update

grow_db(repeat=10)
