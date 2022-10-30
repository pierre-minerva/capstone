from django.db import models

#The Frontier database contains a url and boolean field. The purpose is to keep track of urls already scraped and queue urls that have not been scraped to be scraped. 
class Frontier(models.Model):
	url = models.CharField(max_length=255, unique=True)
	searched = models.BooleanField(default=False)