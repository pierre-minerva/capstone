from django.db import models

#The Frontier database contains a url and boolean field. The purpose is to keep track of urls already scraped and queue urls that have not been scraped to be scraped. 
class Frontier(models.Model):
	url = models.CharField(max_length=255, unique=True)
	searched = models.BooleanField(default=False)

class Algorithm(models.Model):
	name = models.CharField(max_length=225, Null=True)
	desc = models.CharField(max_length=1500, Null=True)
	url = models.CharField(max_length=225, unique=True)
	scraped = models.BooleanField(default=False)

#This can be used to represent the network
class Edge(models.Model):
	alg1 = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
	alg2 = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
	weight = models.IntegerField(default=0)