# critics/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms


@login_required
def home(request):
    message = 'Vous êtes connectés !'
    return render(request, 'critics/home.html', context={'message': message})


@login_required
def ticket_create(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'critics/ticket_create.html', context={'ticket_form': ticket_form})
