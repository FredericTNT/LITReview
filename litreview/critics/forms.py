from django import forms
from django.contrib.auth import get_user_model
from . import models


class TicketForm(forms.ModelForm):
    """ Formulaire Ticket """
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    """ Formulaire Critique """
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {'rating': forms.RadioSelect()}


class UserFollowForm(forms.ModelForm):
    """ Formulaire Abonnement """
    class Meta:
        model = get_user_model()
        fields = ['follows']
