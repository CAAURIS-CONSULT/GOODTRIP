from django.db import models
from django.contrib.auth.models import User


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CodeInstance(models.Model):
    Code                    = models.IntegerField()
    associatedUser          = models.CharField(default='username',max_length=20)
    createdAt               = models.DateTimeField(auto_now_add=True)
    already_used            = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Code} du {self.createdAt}'

class Particulier(models.Model):
    user = models.OneToOneField(User, default=1, on_delete=models.CASCADE)
    phone_number            = models.IntegerField(default='2250000000000')
    isVerified              = models.BooleanField(default=False)
    isVerifiable            = models.BooleanField(default=True)
    lastAssociatedCodeGenAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user.last_name and self.user.first_name:
            return f'{self.user.last_name} {self.user.first_name}'
        else: 
            return self.user.username