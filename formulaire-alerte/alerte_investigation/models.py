"""Modèle de données des alertes sanitaires et de leur investigation."""

import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Q


class SourceAlerte(models.TextChoices):
    """Origine d'une alerte."""

    CENTRE_APPEL = "centre_appel", "Centre d'appel"
    SUIVI_CONTACTS = "suivi_contacts", "Suivi des contacts"
    EIIR = "eiir", "EIIR"
    POINT_ENTREE = "point_entree", "Point d'entrée"
    ASC = "asc", "ASC"
    COMMUNAUTE = "communaute", "Communauté"
    FOSA = "fosa", "FOSA"
    AUTRE = "autre", "Autre"


valider_identifiant = RegexValidator(
    regex=r"^[A-Za-z0-9]{9}$",
    message="L'identifiant doit contenir exactement 9 caractères alphanumériques.",
)

_CARACTERES_TELEPHONE = re.compile(r"^\+?[0-9 .()\-]+$")


def valider_telephone(valeur: str) -> None:
    """Accepte chiffres, espaces, points, tirets, parenthèses et un « + » initial.

    Le numéro doit compter de 7 à 15 chiffres (15 étant le maximum de la norme E.164).
    """
    nombre_chiffres = sum(caractere.isdigit() for caractere in valeur)
    if not _CARACTERES_TELEPHONE.match(valeur) or not 7 <= nombre_chiffres <= 15:
        raise ValidationError(
            "Numéro invalide : 7 à 15 chiffres, éventuellement séparés par des espaces, "
            "points, tirets ou parenthèses, avec un « + » initial facultatif.",
            code="telephone_invalide",
        )


class AlerteInvestigation(models.Model):
    """Une alerte reçue et, le cas échéant, son investigation sur le terrain."""

    # --- Alerte -------------------------------------------------------------------------
    identifiant_alerte = models.CharField(
        "ID alerte",
        max_length=9,
        unique=True,
        validators=[valider_identifiant],
        help_text="9 caractères alphanumériques.",
        error_messages={"unique": "Une alerte avec cet identifiant existe déjà."},
    )
    date_notification = models.DateField("date de notification")
    heure_alerte = models.TimeField("heure de l'alerte")
    personne_structure_transmis_alerte = models.CharField(
        "personne (ou structure) ayant transmis l'alerte", max_length=255, blank=True
    )
    numero_telephone = models.CharField(
        "N° de téléphone", max_length=20, blank=True, validators=[valider_telephone]
    )
    source_alerte = models.CharField("source de l'alerte", max_length=20, choices=SourceAlerte.choices)
    source_alerte_precision = models.CharField(
        "précision sur la source",
        max_length=255,
        blank=True,
        help_text="Obligatoire lorsque la source est « Autre ».",
    )

    # --- Investigation ------------------------------------------------------------------
    heure_information_equipe = models.TimeField(
        "heure à laquelle l'équipe d'investigation a été informée", null=True, blank=True
    )
    heure_arrivee_site = models.TimeField(
        "heure à laquelle l'équipe a notifié son arrivée sur le site", null=True, blank=True
    )
    date_investigation = models.DateField("date d'investigation", null=True, blank=True)
    heure_investigation = models.TimeField("heure d'investigation", null=True, blank=True)
    nom_equipe_investigateur = models.CharField(
        "nom de l'équipe ou de l'investigateur", max_length=255, blank=True
    )

    cree_le = models.DateTimeField("enregistrée le", auto_now_add=True)

    class Meta:
        verbose_name = "alerte et investigation"
        verbose_name_plural = "alertes et investigations"
        ordering = ["-date_notification", "-heure_alerte"]
        constraints = [
            models.CheckConstraint(
                condition=Q(date_investigation__isnull=True)
                | Q(date_investigation__gte=F("date_notification")),
                name="investigation_posterieure_notification",
                violation_error_message=(
                    "La date d'investigation ne peut pas être antérieure à la date de notification."
                ),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.identifiant_alerte} ({self.date_notification:%d/%m/%Y})"

    def clean(self) -> None:
        """Contrôles portant sur plusieurs champs."""
        super().clean()
        erreurs = {}
        if (
            self.date_notification
            and self.date_investigation
            and self.date_investigation < self.date_notification
        ):
            erreurs["date_investigation"] = (
                "La date d'investigation ne peut pas être antérieure à la date de notification."
            )
        if self.source_alerte == SourceAlerte.AUTRE and not self.source_alerte_precision.strip():
            erreurs["source_alerte_precision"] = "Précisez la source lorsque « Autre » est sélectionné."
        if erreurs:
            raise ValidationError(erreurs)
