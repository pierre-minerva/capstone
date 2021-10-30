from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import csrf
from . import functions

# Create your views here.
def home(request):
	c = {}
	c.update(csrf(request))

	if request.method == "POST":
		link = request.POST['link']

		content = functions.get_page(link)

		alg_links = functions.get_all_links(content)

		functions.update_related_algs(alg_links)

		related_algs = get_related_algs(alg_links)


		return render(request, 'optalg/home.html',c)

	else:
		return render(request, 'optalg/home.html',c)

def writeup(request):
	return render(request, 'optalg/writeup.html')