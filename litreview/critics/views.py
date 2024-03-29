# critics/views.py
from itertools import chain
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rules.contrib.views import permission_required, objectgetter
from django.views.generic import View
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from . import forms
from authentication.models import User
from critics.models import Ticket, Review


@method_decorator(permission_required('critics.add_ticket'), name='dispatch')
class TicketCreateView(View):
    """ Publier un ticket """
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


@method_decorator(permission_required('critics.change_ticket', fn=objectgetter(Ticket, 'id')), name='dispatch')
class TicketUpdateView(View):
    """ Mettre à jour un ticket """
    template_name = 'critics/ticket_create.html'
    form_class = forms.TicketForm

    def get(self, request, id):
        ticket = Ticket.objects.get(id=id)
        form = self.form_class(instance=ticket)
        messages.info(request, 'Mettre à jour le ticket')
        return render(request, self.template_name, context={'form': form})

    def post(self, request, id):
        ticket = Ticket.objects.get(id=id)
        form = self.form_class(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket mis à jour')
            return redirect('home')
        messages.warning(request, 'Formulaire incomplet !')
        return render(request, self.template_name, context={'form': form})


@method_decorator(permission_required('critics.delete_ticket', fn=objectgetter(Ticket, 'id')), name='dispatch')
class TicketDeleteView(View):
    """ Supprimer un ticket avec demande de confirmation """
    template_name = 'critics/ticket_delete.html'

    def get(self, request, id):
        ticket = Ticket.objects.get(id=id)
        messages.info(request, 'Confirmer la suppression')
        return render(request, self.template_name, context={'ticket': ticket})

    def post(self, request, id):
        Ticket.objects.get(id=id).delete()
        messages.success(request, 'Ticket supprimé')
        return redirect('home')


@method_decorator(permission_required('critics.add_review'), name='dispatch')
class ReviewCreateView(View):
    """ Publier une critique en réponse à un ticket """
    template_name = 'critics/review_create.html'
    form_class = forms.ReviewForm

    def get(self, request, id):
        form = self.form_class()
        ticket = Ticket.objects.get(id=id)
        messages.info(request, 'Créer une critique')
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})

    def post(self, request, id):
        form = self.form_class(request.POST)
        ticket = Ticket.objects.get(id=id)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, 'Critique publiée')
            return redirect('home')
        messages.warning(request, 'Formulaire incomplet !')
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})


@method_decorator(permission_required('critics.change_review', fn=objectgetter(Review, 'id')), name='dispatch')
class ReviewUpdateView(View):
    """ Mettre à jour une critique """
    template_name = 'critics/review_create.html'
    form_class = forms.ReviewForm

    def get(self, request, id):
        review = Review.objects.get(id=id)
        if review.user != request.user:
            return redirect('home')
        form = self.form_class(instance=review)
        messages.info(request, 'Mettre à jour la critique')
        return render(request, self.template_name, context={'form': form, 'ticket': review.ticket})

    def post(self, request, id):
        review = Review.objects.get(id=id)
        form = self.form_class(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Critique mise à jour')
            return redirect('home')
        messages.warning(request, 'Formulaire incomplet !')
        return render(request, self.template_name, context={'form': form, 'ticket': review.ticket})


@permission_required('critics.delete_review', fn=objectgetter(Review, 'id'))
def review_delete(request, id):
    """ Supprimer une critique sans confirmation """
    Review.objects.get(id=id).delete()
    messages.success(request, 'Critique supprimée')
    return redirect('home')


decorators = [permission_required('critics.add_ticket'), permission_required('critics.add_review')]


@method_decorator(decorators, name='dispatch')
class TicketReviewCreateView(View):
    """ Publier un ticket et une critique (processus unique) """
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
    """ Gérer les abonnements """
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
    """ Supprimer un abonnement sans confirmation """
    request.user.follows.remove(User.objects.get(id=id))
    messages.success(request, 'Abonnement supprimé')
    return redirect('home')


class PostView(LoginRequiredMixin, View):
    """ Afficher les publications de l'utilisateur """
    template_name = 'critics/post.html'

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)
        posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)
        messages.info(request, 'Vos publications')
        return render(request, self.template_name, context={'posts': posts})


class FluxView(LoginRequiredMixin, View):
    """ Afficher le flux de l'utilisateur """
    template_name = 'critics/flux.html'

    def get(self, request):
        followings = request.user.follows.all()
        reviews = Review.objects.filter(Q(user=request.user) | Q(user__in=followings) | Q(ticket__user=request.user))
        tickets = Ticket.objects.filter(Q(user=request.user) | Q(user__in=followings)).exclude(Q(review__in=reviews))
        posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, context={'page_obj': page_obj})
