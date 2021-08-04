from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib import messages
import requests
import random

# Create your views here.

@login_required()
def dashboard(request):
    return render(request, "users/dashboard.html")

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
    return render(request, 'users/phone_form.html')
    