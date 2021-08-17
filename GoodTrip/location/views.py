from django.shortcuts import render, redirect
from location.models import Marque, Modele, Vehicule, Category
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
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
    return JsonResponse({'models':listModel})

def rechercheVoiture(request):
        if request.method  == 'GET':
            modele = request.GET.get('modeles')
            marque = request.GET.get('marque')
            category = request.GET.get('category')
            marqueId = Marque.objects.filter(nom_marque = marque)
            modeleId = Modele.objects.filter(nom_modele = modele)
            categoryId = Category.objects.filter(nom_category = category)

            params = Q(category=categoryId)
            params.add(Q(marque=marqueId),Q.AND)
            params.add(Q(modele=modeleId),Q.AND)

            resultat = Vehicule.objects.filter(params)
            context = {
                'resultat':resultat,
            }
            return render(request, 'achat-vehicule-grille.html', context)
        else:
            return redirect('acc_location')
