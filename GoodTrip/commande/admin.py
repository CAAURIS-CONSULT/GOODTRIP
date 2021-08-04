from django.contrib import admin
from .models import Vehicule, Colis, Marque, Modele, Category
# Register your models here.
admin.site.register(Vehicule)
admin.site.register(Colis)
admin.site.register(Modele)
admin.site.register(Marque)
admin.site.register(Category)