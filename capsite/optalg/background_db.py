from optalg import data_functions
from background_task import background
from optalg import models
import time
import networkx as nx

#A frontier based chronic update appraoch where we take the first listed algorithm page to scrape that hasn't already been scraped and scrape it.
#The decorator is from the background_task module that runs the function in the background.
@background(schedule=100)
def grow_db():
	new_alg_obj = models.Frontier.filter(searched=False)[0]
	Update = functions.WebScraper(url=new_alg_obj.url, run=True)
	del Update

grow_db(repeat=100)
