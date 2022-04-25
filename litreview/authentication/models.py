# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """ Utilisateur générique django + photo de profil """
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    follows = models.ManyToManyField('self', through='UserFollows', symmetrical=False)


class UserFollows(models.Model):
    """ Table relation m2m Abonnement/Abonné """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
