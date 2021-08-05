#from django.conf.urls import url
from users.views import dashboard, register, confirmPhoneNumber, registerNumber, registerParticulier
from django.urls import path, include
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('phone/',confirmPhoneNumber,name='register_phone'),
    path('particulier/', registerParticulier, name = 'enregistrerParticulier'),
]