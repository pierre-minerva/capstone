from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import csrf
from optalg import data_functions

#The home page
def home(request):
	return render(request, 'optalg/home.html')

#The main app page
def app(request):
	#The csrf token provided is due to the POST method used on this page. It is necessary based on Django's built-in security features.
	c = {}
	c.update(csrf(request))

	#If someone inputs an algorithm link to find alternates for, it is submitted through a POST request, 
	#the backend finds alternates using the functions.return_related_algs function, then returns the related algs. 
	if request.method == "POST":
		link = request.POST['link']

		related_algs = data_functions.return_related_algs(link)
		c["related_algs"]  = related_algs

		return render(request, 'optalg/app.html',c)

	else:
		return render(request, 'optalg/app.html',c)

#The writeup page
def writeup(request):
	return render(request, 'optalg/writeup.html') 