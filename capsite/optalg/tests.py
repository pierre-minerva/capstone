from django.test import TestCase
from optalg.models import Algorithm, Edge

# Create your tests here.
class AlgorithmTestCase(TestCase):
	def setUp(self):
		Algorithm.objects.create(url="https://www.test.com")
		Algorithm.objects.create(name="Test", desc="Test test", url="www.test.com", scraped=True)
		