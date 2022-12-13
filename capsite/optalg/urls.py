from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="optalg-home"),
	path('home/', views.home, name="optalg-home"),
	path('app/', views.app, name="optalg-app"),
	path("writeup/", views.writeup, name="optalg-writeup"),
]

#Schedule background_tasks
from . import background_db
background_db.grow_db()