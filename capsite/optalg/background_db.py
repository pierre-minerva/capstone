from optalg import data_functions
from background_task import background
from optalg import models
import time
import networkx as nx

#A frontier based chronic update appraoch where we take the first listed algorithm page to scrape that hasn't already been scraped and scrape it.
#The decorator is from the background_task module that runs the function in the background.
@background(schedule=100)
def grow_db():
	#We get the new algorithm to scrape at the top of the list.
	new_alg_obj = models.Frontier.filter(searched=False)[0]
	#We scrape it, collecting information on it and adding new algorithms found to the frontier, and remove it from the list.
	Update = data_functions.WebScraper(url=new_alg_obj.url)
	#Delete the class instance to prevent bloat. 
	del Update

#Call the background function and schedule it to repeat every 100s. 
grow_db(repeat=100)
