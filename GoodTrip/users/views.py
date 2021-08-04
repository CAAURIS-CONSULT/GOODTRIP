from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib import messages
import requests
import random
import json

# Create your views here.

@login_required()
def dashboard(request):
    return render(request, "users/dashboard.html")

def sendMessage(message, phone_number):
    url = "https://api.letexto.com/v1/campaigns"

    headers = {
            'Authorization': 'Bearer 2145f4b909bdabcfa8fdac20bb17ad',
            'Content-Type': 'application/json'
            }
    payload={"step": 'null',
            "sender": 'GoodTrip',
            "name": "GoodTrip",
            "campaignType": "SIMPLE",
            "recipientSource": "CUSTOM",
            "groupId": 'null',
            "filename": 'null',
            "saveAsModel": 'false',
            "destination": "NAT_INTER",
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
    #sending_url = f'https://api.letexto.com/v1/campaigns/{id}'
    headers2 = { 'Authorization': 'Bearer 2145f4b909bdabcfa8fdac20bb17ad' }
    payload2={}
    sendind_response = requests.request("POST",sending_url,headers=headers2,data={})
    return sendind_response

def registerNumber(request):
    return render(request, 'users/phone_form.html')

def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            message = messages.success(request, f'utilisateur {{ username }} créé avec succès')
            return redirect('dashboard')
    return render(request, 'registration/register_final.html', {'form':form})

def confirmPhoneNumber(request):
#    return render(request,'phone_verification.html',{'reponse':response})
    if request.method=='POST':
        Code = random.randrange(100000,999999)
        if request.POST.get('phoneNumber'):
            #url = 'https://api.letexto.com/v1/dev/campaigns'
            Message = f'Votre code de vérification est:\n{Code}'
            phoneNumber = request.POST['phoneNumber']
            response = sendMessage(Message,phoneNumber)
            return render(request, 'users/verification_form.html', {'reponse':response.text})
        elif request.POST.get('receivedCode'):
            receivedCode = request.POST['receivedCode']
            if str(Code) == str(receivedCode):
                return render(request, 'users/ok.html')
            else:
                #errorMessage = messages
                return render(request,'users/phone_form.html', {'code':receivedCode})
    else:
        return render(request,'users/phone_form.html')