import data_functions
from background_task import background
from . import models
import time
import networkx as nx

#A frontier based chronic update appraoch where we take the first listed algorithm page to scrape that hasn't already been scraped and scrape it.
#The decorator is from the background_task module that runs the function in the background.
@background(schedule=1000)
def grow_db():
	#This page is used to kickstart the database.  It contains a list of algorithms
	# We check if we already initialized the db collection start point
	if models.Frontier.objects.filter(url = "https://en.wikipedia.org/wiki/List_of_algorithms").exists():
		#We get the new algorithm to scrape at the top of the list.
		new_alg_obj = models.Frontier.filter(searched=False)[0]
		#We scrape it, collecting information on it and adding new algorithms found to the frontier, and remove it from the list.
		Update = data_functions.WebScraper(url=new_alg_obj.url)
		#Delete the class instance to prevent bloat. 
		del Update
	else:
		#We run the Update class
		Update = data_functions.WebScraper(url="https://en.wikipedia.org/wiki/List_of_algorithms")
		del Update

	

#Call the background function and schedule it to repeat every 100s. 
grow_db(repeat=100)
