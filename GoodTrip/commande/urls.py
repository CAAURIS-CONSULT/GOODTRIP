#from django.conf.urls import url
from commande.views import listingView  
from django.urls import path, include
urlpatterns = [
    path('vehicules/',listingView,name='vehicules'),
]