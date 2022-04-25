from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Ticket(models.Model):
    """ Modèle Ticket """
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True, verbose_name="Description")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, verbose_name="Photo du livre ou de l'article")
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    """ Modèle Critique """

    class Notation(models.IntegerChoices):
        ZERO = 0, _('0')
        UN = 1, _('1')
        DEUX = 2, _('2')
        TROIS = 3, _('3')
        QUATRE = 4, _('4')
        CINQ = 5, _('5')
        __empty__ = _('')

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=Notation.choices, verbose_name='Note')
    headline = models.CharField(max_length=128, verbose_name='Titre')
    body = models.TextField(max_length=8192, blank=True, verbose_name='Commentaire')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
