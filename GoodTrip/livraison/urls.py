from django.urls import path
from livraison.views import accueil

urlpatterns = [
    path('', accueil, name='acc_livraison'),
]
