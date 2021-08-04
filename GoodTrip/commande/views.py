from django.shortcuts import render
from .models import Vehicule
# Create your views here.
def listingView(request):
    vehicule = Vehicule.objects.all()
    liste = []
    for v in vehicule:
        liste.append({'vehicule':v,'subdesc':v.description[:100]+'...'})

    return render(request,'commande/vehicules.html',{'vehicules':liste})