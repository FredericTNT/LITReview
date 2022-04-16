# critics/views.py
from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib import messages
from django.db.models import Value, CharField, Q
from . import forms
from authentication.models import User
from critics.models import Ticket, Review


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


class TicketReviewCreateView(LoginRequiredMixin, View):
    template_name = 'critics/ticket_review_create.html'
    form_ticket = forms.TicketForm
    form_review = forms.ReviewForm

    def get(self, request):
        ticket_form = self.form_ticket()
        review_form = self.form_review()
        messages.info(request, 'Publier une critique')
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


class UserFollowView(LoginRequiredMixin, View):
    template_name = 'critics/user_follow.html'
    form_class = forms.UserFollowForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        followings = request.user.follows.all()
        followers = request.user.user_set.all()
        messages.info(request, 'Abonnements')
        context = {'form': form, 'followings': followings, 'followers': followers}
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            for user in form.cleaned_data['follows']:
                if user != request.user:
                    request.user.follows.add(user)
            messages.success(request, 'Abonnement enregistré')
            return redirect('home')
        messages.warning(request, 'Formulaire incomplet !')
        return render(request, self.template_name, context={'form': form})


@login_required
def user_follow_delete(request, id):
    request.user.follows.remove(User.objects.get(id=id))
    messages.success(request, 'Abonnement supprimé')
    return redirect('home')


class PostView(LoginRequiredMixin, View):
    template_name = 'critics/post.html'

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)
        messages.info(request, 'Vos publications')
        return render(request, self.template_name, context={'posts': posts})


class FluxView(LoginRequiredMixin, View):
    template_name = 'critics/flux.html'

    def get(self, request):
        followings = request.user.follows.all()
        reviews = Review.objects.filter(Q(user=request.user) | Q(user__in=followings) | Q(ticket__user=request.user))
        tickets = Ticket.objects.filter(Q(user=request.user) | Q(user__in=followings)).exclude(Q(review__in=reviews))
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)
        return render(request, self.template_name, context={'posts': posts})
