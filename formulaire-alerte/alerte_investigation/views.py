"""Vues de l'application."""

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import AlerteInvestigationForm


def saisir_alerte(request):
    """Affiche le formulaire et enregistre l'alerte (motif Post/Redirect/Get)."""
    if request.method == "POST":
        form = AlerteInvestigationForm(request.POST)
        if form.is_valid():
            alerte = form.save()
            messages.success(request, f"L'alerte {alerte.identifiant_alerte} a bien été enregistrée.")
            return redirect("alerte_investigation:saisie")
    else:
        form = AlerteInvestigationForm()
    return render(request, "alerte_investigation/alerte_form.html", {"form": form})
