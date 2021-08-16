from django.shortcuts import render
from location.models import Marque, Modele, Vehicule, Category
from django.http import HttpResponse
# Create your views here.
def accueil(request):
    template_name = 'location/accueil.html'
    listModel       = Modele.objects.all()
    listMarque      = Marque.objects.all()
    listCategory    = Category.objects.all()
    context = {
        'modeles':listModel,
        'marques':listMarque,
        'category':listCategory,
    }
    return render(request,template_name, context)
def ajaxView(request):
    if request.is_ajax():
        pass