from django.contrib import admin

from .models import Registration, RegistrationAdmin

# Register your models here.

admin.site.register(Registration, RegistrationAdmin)
