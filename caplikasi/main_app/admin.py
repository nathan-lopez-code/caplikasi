from django.contrib import admin
from .models import Client, Archivist, CustomUser

admin.site.register(Client)
admin.site.register(Archivist)
admin.site.register(CustomUser)
