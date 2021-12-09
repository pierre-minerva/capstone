from django.db import models

# Create your models here.
class Frontier(models.Model):
	url = models.CharField(max_length=255, unique=True)
	searched = models.BooleanField(default=False)