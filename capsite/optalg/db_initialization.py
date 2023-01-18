import os
import sys
sys.path.append("./optalg")
from background_task import background
import models
import data_functions
import time


def init_db():
	#This page is used to kickstart the database.  It contains a list of algorithms
	wiki_algs_list = "https://en.wikipedia.org/wiki/List_of_algorithms"

	#We run the Update class
	Update = data_functions.WebScraper(url=wiki_algs_list)
	del Update
