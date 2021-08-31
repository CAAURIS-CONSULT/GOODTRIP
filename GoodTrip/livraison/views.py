from django.shortcuts import render

# Create your views here.
def accueil(request):
    template_name = 'livraison/accueil.html'
    return render(request, template_name)