from django.db import models
import datetime
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
    image               =models.ImageField(null=True)
    per_day_price       =models.DecimalField(max_digits=10,decimal_places=2)
    description         =models.TextField(null=True)
    kilometrage         =models.PositiveSmallIntegerField(default=15000)

    def __str__(self):
        return str(self.marque)+" "+str(self.modele)

class Colis(models.Model):
    destination        =models.CharField(max_length=150)
    provenance         =models.CharField(max_length=150)
    forme              =models.CharField(max_length=10)

    def __str__(self):
        return "Colis "+str(self.id)
