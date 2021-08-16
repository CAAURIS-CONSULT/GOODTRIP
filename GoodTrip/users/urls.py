#from django.conf.urls import url 
from users.views import dashboard, registerParticulier, verify_number, LoginView, LogoutView, verifier_code
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    #path('register/', register, name='register'),
    path('accueil/', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),
    #path('phone/',confirmPhoneNumber,name='register_phone'),
    path('register/', registerParticulier, name = 'register'),
    path('verification/',verifier_code,name='verify_number'),
    #path('verification/',verify_number,name='verify_number'),
    path('connexion/',LoginView.as_view(),name='user_login'),
    path('deconnexion/', LogoutView.as_view(),name = 'user_logout')
]