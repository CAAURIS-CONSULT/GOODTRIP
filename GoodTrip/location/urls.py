from django.urls import path
from location.views import accueil, ajaxView, rechercheVoiture, details
urlpatterns = [
    path("", accueil, name="acc_location"),
    path("marque",ajaxView,name="marque"),
    path('recherche', rechercheVoiture, name = 'rechercheVoiture'),
    path('details/<int:id>/',details, name='details')
]