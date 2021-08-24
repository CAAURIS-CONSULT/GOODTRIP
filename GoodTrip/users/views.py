from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Particulier, CodeInstance
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.conf import settings


import requests
import random
import json
import datetime

class LoginView(TemplateView):
    template_name = 'users/dashboard.html'

    def post(self, request, **kwargs):
        username = request.POST.get('id_username')
        password = request.POST.get('id_password')
        if password and username:
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                message = f'Connecté en tant que {user.last_name} {user.first_name}'
                return redirect(request.POST.get('next'))
                #return render(request,self.template_name,{'message':message})
            else:
                error = 'Nom d\'utilisateur ou mot de passe incorrect'
                return render(request, self.template_name, {'error':error,'anchor':'signin-modal'})
        else:
            error = 'Veuillez renseigner les champs ci-dessous'
            return render(request, self.template_name, {'error':error,'anchor':'signin-modal'})

class LogoutView(TemplateView):

  template_name = settings.LOGOUT_REDIRECT_URL

  def get(self, request, **kwargs):

    logout(request)

    return redirect(request.POST.get('next'))


# Create your views here.

#@login_required()
def dashboard(request):
    return render(request, "users/dashboard.html")

def sendMessage(message, phone_number):
    url = "https://api.letexto.com/v1/campaigns"

    headers = {
            'Authorization': 'Bearer 2145f4b909bdabcfa8fdac20bb17ad',
            'Content-Type': 'application/json'
            }
    payload={
            "step": 'null',
            "sender": 'GoodTrip',
            "name": "GoodTrip",
            "campaignType": "SIMPLE",
            "recipientSource": "CUSTOM",
            "groupId": 'null',
            "filename": 'null',
            "saveAsModel": 'false',
            #"destination": "NAT_INTER",
            "destination": "NAT",
            "message": message,
            "emailText": 'null',
            "recipients": [{"phone":str(phone_number)}],
            "sendAt": [],
            "dlrUrl": "",
            "responseUrl": ""}
    response = requests.request("POST",url,headers=headers,data=json.dumps(payload))
    response_json = response.json()
    identifiant = response_json['id']
    sending_url = f'https://api.letexto.com/v1/campaigns/{identifiant}/schedules'
    headers2 = { 'Authorization': 'Bearer 2145f4b909bdabcfa8fdac20bb17ad' }
    sendind_response = requests.request("POST",sending_url,headers=headers2,data={})
    return sendind_response


def verifier_code(request, username=""):
    template_name = 'users/validation2.html'
    if username =='' and not request.POST.get('username'):
        #Si la vue est sollicitée sans params, alors nous faisons 
        # Une vérification ou ou une réinitialisation de mdp
        context = {
            'motif':'Réinitialisation'
        }
        return render(request, template_name , context)
    if username == '' and request.POST.get('username'):
        error = verifyNumber(request.POST.get('username'))
        if error:
            context = {
                'error':error,
                'motif':'Vérification',
                'username':username
            }
            return render(request, template_name, context)
        username     = str(request.POST.get('username'))
        usernameBack = 'user_225'+username
        if not isUserRegistered(usernameBack):
            context = {
                'error':'Cet utilisateur n\'existe pas.\nVeuillez vous enregistrer',
                'anchor':'signup-modal',
            }
            return render(request, 'users/dashboard.html',context)
        canUserGenCode = canUserGenNewCode(usernameBack)
        if type(canUserGenCode)==int:
            context = {
                'error':'Trop de tentavites !\nVeuillez patienter avant de pouvoir générer un autre code',
                'errcode':'impToGenCode',
                'motif':'réinitialisation',
                'time':canUserGenCode
            }
            return render(request, template_name, context)
        if request.POST.get('code'):
            code = request.POST.get('code')
            error = verification_code(usernameBack,code)
            if type(error) != list:
                user = error
                login(request,user)
                message = 'Votre compte vérifié avec succès'
                context = {
                    'message': message
                }
                return render(request, 'users/dashboard.html', context)
            else:
                print(error)
                context = {
                    'username':username,
                    'motif':'Vérification',
                }
                if error[0]=='impToGenCode':
                    err = 'Trop de tentavites !\nVeuillez patienter avant de pouvoir générer un autre code'
                    time_to_wait = error[1]
                    context['time']=time_to_wait
                if error[0] == 'nocode':
                    err = 'Impossible de verifier ce numéro'
                if error[0] == 'expired':
                    err = 'Ce code a expiré'
                if error[0] == 'incorrect':
                    err = 'Le code entré est incorrect '
                context['error']=err
                context['errcode'] = error[0]
                return render(request, template_name, context)
        
        context = {
            'error':'Saissisez le code recu',
            'motif':'Vérification',
            'username':username,
        }
        code = generateCode(username)
        print(username)
        print(code)
        return render(request,template_name,context)
    if username:
        if len(username)>10:
            username = username.split('_225')[1]
        context = {
            'username':username,
            'motif':'Vérification'
        }
        return render(request,template_name,context)

def verification_code(username,code):
    if not isUserRegistered(username):
        return ['notRegistered']
    if canUserGenNewCode(username) != True:
        return ['impToGenCode', canUserGenNewCode(username)]
    main = CodeInstance.objects.filter(associatedUser=username)
    if len(main) <= 0:
        return ['nocode']
    instanceOfcode = main[len(main)-1]
    print(instanceOfcode.Code)
    if str(instanceOfcode.Code) != str(code):
        return ['incorrect']
    if not isCodeValid(instanceOfcode):
        return ['expired']
    user = User.objects.filter(username=username)[0]
    default_password = User.objects.make_random_password()
    instanceOfcode.already_used = True
    instanceOfcode.save()
    user.set_password(default_password)
    user.save()
    user = authenticate(username=username, password=default_password)
    msg = f'Compte vérifié.\nNom d\'utilisateur: {username}\nMot de passe: {default_password}\nVous pourrez changer votre mot de passe plus tard dans les réglages'
    #sendMessage(msg,username.split('_')[1])
    print(msg)
    return user

def registerParticulier(request):
    # Si l'utilisateur nous envoie des données
    template_name = 'users/dashboard.html'
    if request.method=='POST':
        if request.POST.get('last_name') and request.POST.get('first_name') and request.POST.get('phone_number'):
            # Récupération des données transmises par l'utilisateur dans la requete POST
            last_name       = request.POST.get('last_name')
            first_name      = request.POST.get('first_name')
            phone_number    = request.POST.get('phone_number')
            error = verifyNumber(phone_number)
            if not error:
                username        = f'user_225{phone_number}' # Génère un nom d'utilisateur basé sur son numéro
                user            = User()
                user.username   = username
                user.first_name = first_name
                user.last_name  = last_name
                #user.set_password(default_password)
                if User.objects.filter(username=username):
                    error ='Ce numéro a déjà été utilisé pour une inscription'
                    context = {
                        'error':error,
                        'anchor':'signup-modal',
                        'verif':True
                    }
                    return render(request, template_name, context)
                else:
                    user.save()
                    particulier = Particulier()
                    particulier.phone_number= phone_number
                    particulier.isVerified = False
                    particulier.user = user
                    particulier.save()
                    code = generateCode(username)
                    #sendMessage(f'Votre code est:\n{code}',f'225{phone_number}')
                    print(f'Votre code est:\n{code}')
                    
            else:
                return render(request, template_name, {'error':error, 'anchor':'signup-modal'})
        else:
            error = 'Veuillez resneigner les champs ci-dessous'
            return render(request, template_name, {'error':error, 'anchor':'signup-modal'})

        # Dans le cas contraire, on le dirige vers la page pour nous envoyer ces données
        ## return verify_number(request, username)
        return verifier_code(request, username)
        #return render(request, 'users/verification_form.html')
    else:
        return render(request,template_name)

def verifyNumber(phone_number):
    for car in phone_number:
        if car not in '0123456789':
            return 'Le numéro ne doit contenir que des chiffres'
    if len(phone_number) != 10:
        return 'Le format de numéro doit être de 10 chiffres'
    if phone_number[:2] != '01' and phone_number[:2] != '05' and phone_number[:2] != '07':
       return 'Le numéro doit commencer par 01, 05 ou 07'
    return None

# Générateur de Code pseudo aléatoire
def generateCode(usernane):
    codeToSend = random.randrange(100000,999999)
    code = CodeInstance()
    code.Code = codeToSend
    code.associatedUser =  usernane
    code.save()
    return codeToSend

# Verication de la validité d'un code dument généré.
def isCodeValid(code):
    actual_time = datetime.datetime.now(datetime.timezone.utc)
    delta = actual_time-code.createdAt
    if delta.total_seconds()>300 or code.already_used==True:
        return False
    return True

def canUserGenNewCode(username):
    codeInstances = CodeInstance.objects.filter(associatedUser=username)
    numberOfGeneratedCode = len(codeInstances)
    if numberOfGeneratedCode == 0:
        return True
    lastGeneratedCode = codeInstances[numberOfGeneratedCode-1]
    delta = datetime.datetime.now(datetime.timezone.utc) - lastGeneratedCode.createdAt
    formula = 30*4**(numberOfGeneratedCode-3)
    if numberOfGeneratedCode<=2 or delta.total_seconds()>=formula:
        return True
    return int(formula-delta.total_seconds())

def isUserRegistered(username):
    return len(User.objects.filter(username=username))>0