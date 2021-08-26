from django.db import models
from users.models import Particulier
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Category(models.Model):
    nom_category        = models.CharField(max_length=100)
    def __str__(self):
        return self.nom_category
class Marque(models.Model):
    nom_marque          = models.CharField(max_length=100)
    def __str__(self):
        return self.nom_marque
    
class Modele(models.Model):
    nom_modele          = models.CharField(max_length=100)
    marque              = models.ForeignKey(Marque,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.nom_modele
class Vehicule(models.Model):
    category            =models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    marque              =models.ForeignKey(Marque,on_delete=models.SET_NULL,null=True)
    modele              =models.ForeignKey(Modele,on_delete=models.SET_NULL,null=True,)
    climatisation       =models.BooleanField()
    is_auto             =models.BooleanField(default=False)
    estAVendre          =models.BooleanField(default=False)
    estALouer           =models.BooleanField(default=False)
    per_day_price       =models.DecimalField(max_digits=10,decimal_places=2)
    description         =models.TextField(null=True)
    kilometrage         =models.PositiveSmallIntegerField(default=15000)

    def __str__(self):
        return str(self.marque)+" "+str(self.modele)
class Image(models.Model):
    associatedVehicule = models.ForeignKey(Vehicule,on_delete=models.CASCADE)
    image = models.ImageField(default=False)
    def __str__(self):
        return str(self.associatedVehicule)
        
class Commande(models.Model):    
    user                =models.ForeignKey(User, on_delete=models.CASCADE)
    status              =models.CharField(default='En cours', max_length=100)
    delivered_at        =models.DateField(auto_now_add=True)
    created_at          =models.DateField(auto_now_add=True)
class ProduitCommande(models.Model):
    associatedCommande  =models.ForeignKey(Commande,on_delete=models.CASCADE)
    associateVvehicule  =models.ForeignKey(Vehicule,on_delete=models.CASCADE)
    quantity            =models.IntegerField()
