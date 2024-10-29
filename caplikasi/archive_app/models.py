from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from main_app.models import Archivist

COMMUNE_LIKASI = [
    ("kikula", "Kikula"),
    ("Likasi", "Likasi"),
    ("Panda", "Panda"),
    ("Shituru", "Shituru"),
]

ETAT = [
    ("Bonne", "Bonne"),
    ("Moyen", "Moyen"),
    ("Mauvaise", "Mauvaise"),
    ("En Rehabitation", "En Rehabitation"),
]


class Patrimoine(models.Model):
    # adresse
    avenue = models.CharField(max_length=200)
    numero = models.IntegerField()
    commune = models.CharField(max_length=10, choices=COMMUNE_LIKASI)

    # Caracteristiques physique
    annee_construction = models.IntegerField(
        verbose_name="annee de construction", validators=[MinValueValidator(1700)], blank=True, null=True)
    architecte = models.CharField(max_length=100, blank=True, null=True)
    etat_conservation = models.CharField(max_length=15, choices=ETAT)

    # Informations liées à l'utilisation
    affectation_actuel = models.CharField(max_length=200, )

    # description textuel
    observation = models.CharField(max_length=200, default="aucunne obeservation")

    # images & plan
    image = models.ImageField(upload_to="patrimoine/", blank=True, null=True)


class Fichier_plan(models.Model):
    fichier = models.FileField(upload_to="plan/", )
    patrimoine = models.ForeignKey(Patrimoine, on_delete=models.CASCADE)


class Archive(models.Model):
    titre = models.CharField(max_length=100)
    date_creation = models.DateField(auto_now_add=True)
    archiviste = models.ForeignKey(Archivist, on_delete=models.CASCADE)
    historique = models.TextField(blank=True, null=True)
    patrimoine = models.OneToOneField(Patrimoine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titre} cree par {self.archiviste.user.username}"

    def get_absolute_url(self):
        return reverse("main_app:archive_detail", kwargs={"pk": self.pk})

