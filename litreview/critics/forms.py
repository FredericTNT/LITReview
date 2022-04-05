from django import forms
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {'title': forms.TextInput(attrs={'size': '40'}),
                   'description': forms.Textarea(attrs={'cols': '64'})}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {'headline': forms.TextInput(attrs={'size': '40'}),
                   'rating': forms.RadioSelect(),
                   'body': forms.Textarea(attrs={'cols': '64'})}
