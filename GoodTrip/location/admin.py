from django.contrib import admin
from location.models import Marque, Modele, Category, Vehicule, Image

# Register your models here.
admin.site.register(Marque)
admin.site.register(Modele)
admin.site.register(Category)
admin.site.register(Vehicule)
admin.site.register(Image)