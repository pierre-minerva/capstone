from django.core.management.base import BaseCommand, CommandError
from background_task import background
from optalg import data_functions

class Command(BaseCommand):
	help = "Initialized the DB"

	def handle(self, *args, **options):
		#This page is used to kickstart the database.  It contains a list of algorithms
		wiki_algs_list = "https://en.wikipedia.org/wiki/List_of_algorithms"

		#We run the Update class
		Update = data_functions.WebScraper(url=wiki_algs_list)
		del Update
	
		self.stdout.write(self.style.SUCCESS('Successfully initiated db'))
