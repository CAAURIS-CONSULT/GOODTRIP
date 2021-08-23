from django.urls import path
from location.views import accueil, ajaxForMarques, rechercheVoiture, detailsVehicule
urlpatterns = [
    path("", accueil, name="acc_location"),
    path("marque",ajaxForMarques,name="marque"),
    path('recherche', rechercheVoiture, name = 'rechercheVoiture'),
    path('details/<int:id>/',detailsVehicule, name='details')
]