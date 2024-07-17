# django_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("predictions/", include('predictions.urls')),
    path("knockout/", include('knockout.urls', namespace='knockout')),
    path("gym/", include('gym.urls')),
    path("", include("pages.urls")),
]
