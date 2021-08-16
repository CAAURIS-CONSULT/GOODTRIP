from django.shortcuts import render
from location.models import Marque, Modele, Vehicule, Category
from django.http import HttpResponse, JsonResponse
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
    marque = request.GET.get('marque')
    idMarque = Marque.objects.filter(nom_marque=marque)[0].id
    listModel = [Modele.objects.filter(marque=idMarque)[i].nom_modele for i in range(len(Modele.objects.filter(marque=idMarque)))]
    
    print(listModel)
    return JsonResponse({'models':listModel})