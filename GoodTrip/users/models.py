from django.db import models
from django.contrib.auth.models import User


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CodeInstance(models.Model):
    Code                    = models.IntegerField()
    associatedPhone         = models.IntegerField()
    createdAt               = models.DateTimeField(auto_now_add=True)


class Particulier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber             = models.IntegerField(blank=False, unique=True)
    isVerified              = models.BooleanField(default=False)
    isVerifiable            = models.BooleanField(blank=False)
    lastAssociatedCodeGenAt = models.DateTimeField(auto_now=True)