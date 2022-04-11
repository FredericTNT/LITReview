from django import forms
from django.contrib.auth import get_user_model
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {'rating': forms.RadioSelect()}


class UserFollowForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['follows']
