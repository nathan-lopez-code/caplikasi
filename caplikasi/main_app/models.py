from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


# Tables utilisateurs
# modele de class User parent
class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)


class Client(models.Model):
    """ utilisateur landa du systeme """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} | {self.user.email}"


class Archivist(models.Model):
    """ manager du site d'archivage """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_archivist = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} | {self.user.email}"
