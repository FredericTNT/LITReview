# authentication/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    """ Formulaire de connexion """
    username = forms.CharField(max_length=128, label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Nom utilisateur', 'size': '40'}))
    password = forms.CharField(max_length=128, label="",
                               widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'size': '40'}))


class SignupForm(UserCreationForm):
    """ Formulaire d'inscription """
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'profile_photo')
