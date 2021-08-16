from django.contrib import admin
from users.models import Particulier, CodeInstance

# Register your models here.
admin.site.register(Particulier)
admin.site.register(CodeInstance)