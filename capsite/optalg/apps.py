from django.apps import AppConfig
import os
#from . import background_db


class OptalgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    #Defining the app name.
    name = 'optalg'

    #def ready(self):
    #    background_db.grow_db(scheule =60, repeat=250)
