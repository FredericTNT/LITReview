# critics/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from . import forms


class HomeView(LoginRequiredMixin, View):
    template_name = 'critics/home.html'

    def get(self, request):
        message = 'Vous êtes connectés !'
        return render(request, self.template_name, context={'message': message})


class TicketCreateView(LoginRequiredMixin, View):
    template_name = 'critics/ticket_create.html'
    form_class = forms.TicketForm

    def get(self, request):
        form = self.form_class()
        message = 'Demander une critique'
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})


class ReviewCreateView(LoginRequiredMixin, View):
    template_name = 'critics/review_create.html'
    form_class = forms.ReviewForm

    def get(self, request):
        form = self.form_class()
        message = 'Créer une critique'
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            return redirect('home')
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
