from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from location.models import Marque, Modele, Vehicule, Category, Image, Commande, ProduitCommande
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from users.views import sendMessage

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
        listModel = [Modele.objects.filter(marque=idMarque)[i].nom_modele for i in range(len(Modele.objects.filter(marque=idMarque)))]
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
        context = {
            'vehicules':listvehicule,
            'marques':marques,
            'link':link,
        }
        return render(request, 'location/recherche-vehicule.html', context)
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

@login_required
def commander(request):
    template_name = 'location/historique.html'
    if request.method != 'GET':
        return HttpResponse('Method not allowed')
    else:
        data = request.GET
        user                = request.user
        vehicule_id         = data.get('vehicule_id')
        quantity            = data.get('quantity')
        commande = creerCommande(user)
        vehicule = Vehicule.objects.filter(id=vehicule_id)[0]
        addToCommand(commande,vehicule,quantity)
        message = 'commande bien effectuée'
        #sendMessage(user.phone)
    context = {
        'message':message
    }
    return HttpResponse(message)
    # return render(request, template_name, context)

def creerCommande(user):
    commande = Commande()
    commande.user = user
    commande.save()
    latestCommande = Commande.objects.latest('id')
    return latestCommande

# Permet l'ajout de uqantité à un article ( voiture d'un commande donnée )
def addToCommand(commande,vehicule,quantity):
    produitCommande = ProduitCommande.objects.filter(associatedCommande=commande.id,associateVvehicule_id=vehicule.id)
    if produitCommande:
        produitCommande = produitCommande[0]
        produitCommande.quantity += quantity
        produitCommande.save()
    else:
        newProduitCommande = ProduitCommande()
        newProduitCommande.associateVvehicule = vehicule
        newProduitCommande.associatedCommande = commande
        newProduitCommande.quantity = quantity
        newProduitCommande.save()

@login_required
def history(request):
    template_name = 'location/historique.html'
    mes_commandes = Commande.objects.filter(user = request.user.id)
    for commande in mes_commandes:
        commande.image = []
        listProduitCommande = ProduitCommande.objects.filter(associatedCommande=commande.id)
        for produitCommande in listProduitCommande:
            vehiculeId = produitCommande.associateVvehicule.id
            image = Image.objects.filter(associatedVehicule=vehiculeId)[0].image
            commande.image.append(image)
        # produitCommande = ProduitCommande.objects.filter(associatedCommande=commande.id)
        # associatedVehicule = [v for v in Vehicule.objects.filter(id=)]
        # commande.associatedProduct = produitCommande
        # listImage = []
        # for produit in commande.associatedProduct:
        #     id = produit.id
        #     listImage.append(Image.objects.filter(associatedVehicule=id)[0].image)
        # commande.listImage = listImage
    paginator = Paginator(mes_commandes,6)
    page  = request.GET.get('page')
    try:
        listcommandes = paginator.page(page)
        listcommandes.page=page
    except PageNotAnInteger:
        listcommandes = paginator.page(1)
    except EmptyPage:
        listcommandes = paginator.page(paginator.num_pages)
        listcommandes.page=paginator.num_pages
    link = request.get_full_path().split('&page')[0]+'&page='
    context = {
        'mes_commandes':listcommandes,
        'link':link
    }
    return render(request,template_name, context)


def passwordAndSettings(request):
    template_name = 'location/password-settings.html'
    return render(request, template_name)
