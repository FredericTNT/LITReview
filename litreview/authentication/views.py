# authentication/views.py

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.contrib import messages
from . import forms


class LoginPageView(View):
    """ Connecter un utilisateur """
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        messages.success(request, 'Bienvenue aux critiques littéraires !')
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'Flux des publications')
                return redirect(settings.LOGIN_REDIRECT_URL)
        messages.warning(request, 'Identifiants invalides')
        return render(request, self.template_name, context={'form': form})


class SignupPageView(View):
    """ Inscrire un utilisateur """
    template_name = 'authentication/signup.html'
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            messages.success(request, 'Vous êtes connectés !')
            return redirect(settings.LOGIN_REDIRECT_URL)
        messages.warning(request, 'Formulaire incomplet !')
        return render(request, self.template_name, context={'form': form})
