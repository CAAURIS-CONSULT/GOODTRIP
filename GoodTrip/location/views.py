from django.shortcuts import render, redirect
from location.models import Marque, Modele, Vehicule, Category, Image
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def ajaxForMarques(request):
    if request.GET.get('marque'):
        marque = request.GET.get('marque')
        idMarque = Marque.objects.filter(nom_marque=marque)[0].id
        listModel = [Modele.objects.filter(marque=idMarque)[i].nom_modele for i in range(len(Modele.objects.filter(marque=idMarque)))]
    if request.GET.get('id'):
        idMarque = request.GET.get('id')
        print(idMarque)
        listModel = [Modele.objects.filter(marque=idMarque)[i].nom_modele for i in range(len(Modele.objects.filter(marque=idMarque)))]
        print(listModel)
    return JsonResponse({'models':listModel})

def rechercheVoiture(request):
    marques = Marque.objects.all()
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

        resultat = Vehicule.objects.filter(params)
        for v in resultat:
            assImages = Image.objects.filter(associatedVehicule = v.id)
            v.listAssImages = assImages
        paginator = Paginator(resultat,6)
        page  = request.GET.get('page')
        try:
            listvehicule = paginator.page(page)
            listvehicule.page=page
        except PageNotAnInteger:
            listvehicule = paginator.page(1)
        except EmptyPage:
            listvehicule = paginator.page(paginator.num_pages)
            listvehicule.page=paginator.num_pages
        link = request.get_full_path().split('&page')[0]+'&page='
        print(link)
        context = {
            'vehicules':listvehicule,
            'marques':marques,
            'link':link,
        }
        return render(request, 'location/achat-vehicule-grille.html', context)
    else:
        return redirect('acc_location')

def detailsVehicule(request, id):

    template_name = 'location/details_vehicule.html'
    
    vehicule = Vehicule.objects.filter(id=id)[0]
    images = Image.objects.filter(associatedVehicule = id)
    vehicule.listAssImages = images

    latelyAdd = list(Vehicule.objects.all())[0:-10] #Recupération des 9 derniers véhicules ajoutés
    for v in latelyAdd:
        assImg = Image.objects.filter(associatedVehicule=v.id)
        v.listAssImages = assImg
    
    context = {
        'vehicule':vehicule,
        'lastVehicule':latelyAdd
    }
    return render(request, template_name, context)