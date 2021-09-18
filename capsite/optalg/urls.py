from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="optalg-home"),
	path('home/', views.home, name="optalg-home"),
	path("writeup/", views.writeup, name="optalg-writeup"),
]