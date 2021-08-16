from django.urls import path
from location.views import accueil, ajaxView
urlpatterns = [
    path("", accueil, name="acc_location"),
    path("marque",ajaxView,name="marque"),
]