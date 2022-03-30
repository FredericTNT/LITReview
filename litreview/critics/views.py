# critics/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    message = 'Vous êtes connectés !'
    return render(request, 'critics/home.html', context={'message': message})
