from django.test import TestCase
from optalg.models import Algorithm, Edge
from data_functions import WebScraper
import requests

# Create your tests here.
class AlgorithmTestCase(TestCase):
	def setUp(self):
		#creates the database objects we want to test
		Algorithm.objects.create(url="www.test1.com")
		Algorithm.objects.create(name="Test2", desc="Test2 test2", url="www.test2.com", scraped=True)
		
		def test_single_column_entry(self):
			#retrieves the db object to test
			test1 = Algorithm.objects.get(url="www.test1.com")
			#tests the value
			self.assertEqual(test1.url, "www.test1.com")

		def test_complete_entry(self):
			#retreives the db object to test
			test2 = Algorithm.objects.get(url="www.test2.com")
			#tests all values
			self.assertEqual(test2.name, "Test2")
			self.assertEqual(test2.desc, "Test2 test2")
			self.assertEqual(test2.url, "www.test2.com")
			self.assertEqual(test2.scraped, True)

class EdgeTestCase(TestCase):
	def setUp(self):
		#creates the database objects we want to test
		Edge.objects.create(Algorithm.objects.create(url="www.test1.com"), Algorithm.objects.create(name="Test2", desc="Test2 test2", url="www.test2.com", scraped=True))
		
		def test_edge_entry(self):
			#retrieves the db object to test
			alg_obj = Algorithm.objects.get(url="www.test1.com")
			test1 = Edge.objects.get(alg1= alg_obj)
			#tests the value
			self.assertEqual(test1.alg1, alg_obj)
			self.assertEqual(test1.weight, 1)

		def test_edge_weight_increase(self):
			#retrieves the db object to test
			alg_obj = Algorithm.objects.get(url="www.test1.com")
			test1 = Edge.objects.get(alg1= alg_obj)
			#modify weight increase
			test1.weight = 1
			test1.weight = test1.weight + 1
			#tests the value
			self.assertEqual(test1.weight, 2)

class NetworkTestCase(TestCase):
	def setUp(self):
		Scraper = WebScraper(url="https://en.wikipedia.org/wiki/A*_search_algorithm")

		def test_algorithm_node(self):
			self.asssertIsNotNone(Algorithm.objects.get("https://en.wikipedia.org/wiki/A*_search_algorithm"))

		def test_edges(self):
			self.asssertIsNotNone(Edge.objects.get(Q(alg_one="https://en.wikipedia.org/wiki/A*_search_algorithm") | Q(alg_two="https://en.wikipedia.org/wiki/A*_search_algorithm")))
