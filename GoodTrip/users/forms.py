from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserPhoneRegister():
    phone_number = forms.CharField(max_length = 15)

class UserRegistrationForm(UserCreationForm):
    phone_number        = forms.CharField(max_length=20)

    class Meta:
        model           = User
        fields          = ['username', 'email', 'last_name', 'first_name', 'phone_number', 'password1', 'password2']
        widgets         = {
            'username': forms.TextInput(attrs={
                'placeholder':'Nom d\'utilisateur',
                'class': 'form-control mb-3',
            }),
            'email':forms.EmailInput(attrs={
                'placeholder':'Email',
                'class': 'form-control mb-3',
            }),
            'last_name':forms.TextInput(attrs={
                'placeholder':'Nom',
                'class': 'form-control mb-3',
            }),
            'first_name':forms.TextInput(attrs={
                'placeholder':'Prénom',
                'class': 'form-control mb-3',
            }),
            'phone_number':forms.PasswordInput(attrs={
                'id_for_label':'phone_numb',
                'placeholder':'phone number',
                'class':'form-control mb-3'
            })
        }