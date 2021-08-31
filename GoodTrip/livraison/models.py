from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Localisation(models.Model):
    nom_commune     = models.CharField(max_length = 100)

class Trajet(models.Model):
    depart          = models.ForeignKey(Localisation, on_delete=models.CASCADE, related_name='depart')
    arrivee         = models.ForeignKey(Localisation, on_delete=models.CASCADE, related_name='arrivee')
    cout_du_trajet  = models.PositiveIntegerField(default=5)
    distance_approx = models.PositiveIntegerField(default=5)

class Livraison(models.Model):
    proprietaire    = models.ForeignKey(User, on_delete=models.CASCADE)
    trajet          = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    status          = models.CharField(max_length =20, default = 'En cours')