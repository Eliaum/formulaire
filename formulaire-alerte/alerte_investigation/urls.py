"""Routes de l'application."""

from django.urls import path

from . import views

app_name = "alerte_investigation"

urlpatterns = [
    path("", views.saisir_alerte, name="saisie"),
]
