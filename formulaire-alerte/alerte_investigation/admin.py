"""Consultation et gestion des alertes dans l'administration Django."""

from django.contrib import admin

from .models import AlerteInvestigation


@admin.register(AlerteInvestigation)
class AlerteInvestigationAdmin(admin.ModelAdmin):
    list_display = (
        "identifiant_alerte",
        "date_notification",
        "heure_alerte",
        "source_alerte",
        "date_investigation",
        "nom_equipe_investigateur",
    )
    list_filter = ("source_alerte", "date_notification", "date_investigation")
    search_fields = (
        "identifiant_alerte",
        "personne_structure_transmis_alerte",
        "nom_equipe_investigateur",
    )
    date_hierarchy = "date_notification"
    readonly_fields = ("cree_le",)
    fieldsets = (
        (
            "Alerte",
            {
                "fields": (
                    "identifiant_alerte",
                    ("date_notification", "heure_alerte"),
                    ("personne_structure_transmis_alerte", "numero_telephone"),
                    ("source_alerte", "source_alerte_precision"),
                )
            },
        ),
        (
            "Investigation",
            {
                "fields": (
                    ("heure_information_equipe", "heure_arrivee_site"),
                    ("date_investigation", "heure_investigation"),
                    "nom_equipe_investigateur",
                )
            },
        ),
        ("Traçabilité", {"fields": ("cree_le",)}),
    )
