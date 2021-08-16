#from django.conf.urls import url 
from users.views import dashboard, registerParticulier, LoginView, LogoutView, verifier_code
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accueil/', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),
    path('register/', registerParticulier, name = 'register'),
    path('verification/',verifier_code,name='verify_number'),
    path('connexion/',LoginView.as_view(),name='user_login'),
    path('deconnexion/', LogoutView.as_view(),name = 'user_logout')
]