from django.urls import path
from location.views import accueil, ajaxView, rechercheVoiture
urlpatterns = [
    path("", accueil, name="acc_location"),
    path("marque",ajaxView,name="marque"),
    path('recherche', rechercheVoiture, name = 'rechercheVoiture'),
]