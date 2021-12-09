from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import csrf
from optalg import functions

# Create your views here.
def home(request):
	c = {}
	c.update(csrf(request))

	if request.method == "POST":
		link = request.POST['link']

		related_algs = functions.return_related_algs(link)
		print(related_algs)
		c["related_algs"]  = related_algs

		return render(request, 'optalg/home.html',c)

	else:
		return render(request, 'optalg/home.html',c)

def writeup(request):
	return render(request, 'optalg/writeup.html')