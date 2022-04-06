# critics/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages
from . import forms


class HomeView(LoginRequiredMixin, View):
    template_name = 'critics/home.html'

    def get(self, request):
        return render(request, self.template_name)


class TicketCreateView(LoginRequiredMixin, View):
    template_name = 'critics/ticket_create.html'
    form_class = forms.TicketForm

    def get(self, request):
        form = self.form_class()
        messages.info(request, 'Demander une critique')
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Demande de critique envoyée')
            return redirect('home')
        messages.warning(request, 'Formulaire incomplet !')
        return render(request, self.template_name, context={'form': form})


class ReviewCreateView(LoginRequiredMixin, View):
    template_name = 'critics/review_create.html'
    form_class = forms.ReviewForm

    def get(self, request):
        form = self.form_class()
        messages.info(request, 'Créer une critique')
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Critique pas vraiment enregistrée...')
            return redirect('home')
        messages.warning(request, 'Formulaire incomplet !')
        return render(request, self.template_name, context={'form': form})


class CreateTicketReviewView(LoginRequiredMixin, View):
    template_name = 'critics/create_ticket_review.html'
    form_ticket = forms.TicketForm
    form_review = forms.ReviewForm

    def get(self, request):
        ticket_form = self.form_ticket()
        review_form = self.form_review()
        messages.info(request, 'Livre/Article & Critique')
        return render(request, self.template_name, context={'ticket_form': ticket_form, 'review_form': review_form})

    def post(self, request):
        ticket_form = self.form_ticket(request.POST, request.FILES)
        review_form = self.form_review(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, 'Livre/Article & Critique publiés')
            return redirect('home')
        messages.warning(request, 'Formulaire incomplet !')
        return render(request, self.template_name, context={'ticket_form': ticket_form, 'review_form': review_form})
