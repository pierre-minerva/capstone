from django.core.management.base import BaseCommand, CommandError
from background_task import background
from optalg import data_functions

class Command(BaseCommand):
	help = "Initialized the DB"

	def handle(self, *args, **options):
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
	
		self.stdout.write(self.style.SUCCESS('Successfully initiated db'))
