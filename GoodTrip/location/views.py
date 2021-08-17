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
def 
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
            params = Q()
            if Marque.objects.filter(nom_marque = marque):
                marqueId = Marque.objects.filter(nom_marque = marque)[0].id
                params.add(Q(marque=marqueId),Q.AND)

            if Modele.objects.filter(nom_modele = modele):
                modeleId = Modele.objects.filter(nom_modele = modele)[0].id
                params.add(Q(modele=modeleId),Q.AND)

            if Category.objects.filter(nom_category = category):
                categoryId = Category.objects.filter(nom_category = category)[0].id
                params.add(Q(category=categoryId),Q.AND)

            print(params)
            resultat = Vehicule.objects.filter(params)
            context = {
                'vehicules':resultat,
            }
            print('result', resultat)
            return render(request, 'location/achat-vehicule-grille.html', context)
        else:
            return redirect('acc_location')
def details(request, id):
    print(id)
    return HttpResponse('bien')