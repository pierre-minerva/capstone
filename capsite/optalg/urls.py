from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="optalg-home"),
	path('home/', views.home, name="optalg-home"),
	path('app/', views.app, name="optalg-app"),
	path("writeup/", views.writeup, name="optalg-writeup"),
	path('db-init/', views.db_init, name="db-init")
]

#Schedule background_tasks
#from . import background_db
#background_db.grow_db()