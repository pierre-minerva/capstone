from django.core.management.base import BaseCommand, CommandError
from background_task import background
from optalg import data_functions
from optalg import models

class Command(BaseCommand):
	help = "Initialized the DB"

	def handle(self, *args, **options):
		#This page is used to kickstart the database.  It contains a list of algorithms
		# We check if we already initialized the db collection start point
		if not models.Frontier.objects.filter(url = "https://en.wikipedia.org/wiki/List_of_algorithms").exists():
			frontier_obj = models.Frontier.objects.create(url="https://en.wikipedia.org/wiki/List_of_algorithms")
		#We get the new algorithm to scrape at the top of the list.
		new_alg_obj = models.Frontier.objects.filter(searched=False)[0]
		#We scrape it, collecting information on it and adding new algorithms found to the frontier, and remove it from the list.
		Update = data_functions.WebScraper(url=new_alg_obj.url)
		new_alg_obj.searched = True
		new_alg_obj.save()
		#Delete the class instance to prevent bloat. 
		del Update
	
		self.stdout.write(self.style.SUCCESS('Successfully initiated db'))
