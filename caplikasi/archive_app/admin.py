from django.contrib import admin
from .models import Archive, Patrimoine, Fichier_plan


admin.site.register(Archive)
admin.site.register(Fichier_plan)

@admin.register(Patrimoine)
class PatrimoineAdmin(admin.ModelAdmin):
    list_display = ("avenue", "annee_construction", "affectation_actuel","type_construction")
