from django.urls import path
from location.views import accueil
urlpatterns = [
    path("", accueil, name="acc_location")
]