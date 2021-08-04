from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser

class Utilisateur(AbstractBaseUser):
    email                   = models.EmailField(verbose_name = 'email', max_length = 250, unique = True)
    username                = models.CharField(verbose_name = 'Nom d\'utilisateur', max_length = 100)
    phone_number            = models.CharField(verbose_name = 'Numéro de Téléphone', max_length = 13)
    date_inscription        = models.DateTimeField(verbose_name='Inscrit le ', auto_now_add=True)
    nom                     = models.CharField(verbose_name= 'nom', max_length = 100)
    prenom                  = models.CharField(verbose_name = 'prenom', max_length = 100)
    is_admin                = models.BooleanField(default=True)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=True)
    is_superuser            = models.BooleanField(default=True)
    
    USERNAME_FIELD          = 'email'
    REQUIRED_FIELDS         = ['username', 'nom', 'prenom', 'email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        pass