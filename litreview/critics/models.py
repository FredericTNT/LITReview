import rules
from django.db import models
from rules.contrib.models import RulesModel
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from PIL import Image


@rules.predicate
def is_ticket_author(user, ticket):
    """ Verifier si l'utilisateur est l'auteur du ticket """
    return ticket.user == user


class Ticket(RulesModel):
    """ Modèle Ticket étendu aux permissions du package rules """

    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "view": rules.is_authenticated,
            "change": is_ticket_author,
            "delete": is_ticket_author,
        }

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True, verbose_name="Description")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, verbose_name="Photo du livre ou de l'article")
    time_created = models.DateTimeField(auto_now_add=True)

    """ Re-dimensionnement de l'image livre/article via la surcharge de la méthode save """
    IMAGE_MAX_SIZE = (400, 400)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

    def __str__(self):
        return f'{self.id}- {self.title}'


@rules.predicate
def is_review_author(user, review):
    """ Verifier si l'utilisateur est l'auteur de la critique """
    return review.user == user


class Review(RulesModel):
    """ Modèle Critique étendu aux permissions du package rules """

    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "view": rules.is_authenticated,
            "change": is_review_author,
            "delete": is_review_author,
        }

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

    def __str__(self):
        return f'{self.id}- {self.ticket.title} par {self.user.username}'
