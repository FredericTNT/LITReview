"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView, PasswordChangeView
import authentication.views
import critics.views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.png'))),
    path('admin/', admin.site.urls),
    path('', authentication.views.LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('pswchange/', PasswordChangeView.as_view(success_url='/home'), name='password_change'),
    path('signup/', authentication.views.SignupPageView.as_view(), name='signup'),
    path('home/', critics.views.HomeView.as_view(), name='home'),
    path('ticketcreate/', critics.views.TicketCreateView.as_view(), name='ticket_create'),
    path('reviewcreate/', critics.views.ReviewCreateView.as_view(), name='review_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
