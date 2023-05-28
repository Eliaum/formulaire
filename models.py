from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator


class AlerteInvestigation(models.Model):
    """
    Modèle pour stocker les informations sur les alertes et les investigations.
    """

    # Champs pour les alertes et les investigations
    identifiant_alerte = models.CharField(
        max_length=9,
        null=True,
        blank=True,
        validators=[RegexValidator(regex='^[a-zA-Z0-9]{9}$', message='Le champ doit contenir exactement 9 caractères alphanumériques.')],
        verbose_name="ID Alerte"
    )
    date_notification = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de notification"
    )
    numero_telephone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[MinLengthValidator(7)],
        verbose_name="N°Tél"
    )
    heure_alerte = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Heure de l'alerte"
    )
    personne_structure_transmis_alerte = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Personne (ou structure) ayant transmis l'alerte"
    )

    SOURCE_ALERT_CHOICES = [
        ("Centre d'appel", "Centre d'appel"),
        ("Suivi des contacts", "Suivi des contacts"),
        ("EIIR", "EIIR"),
        ("Point d'entrée", "Point d'entrée"),
        ("ASC", "ASC"),
        ("Communauté", "Communauté"),
        ("FOSA", "FOSA"),
        ("Autre", "Autre")
    ]
    source_alerte = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=SOURCE_ALERT_CHOICES,
        verbose_name="Source d'alerte"
    )
    heure_information_equipe = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Heure à laquelle l'équipe d'investigation a été informée"
    )
    heure_arrivee_site = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Heure à laquelle l'équipe d'investigation a notifié son arrivée sur le site"
    )
    date_investigation = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date d'investigation"
    )
    heure_investigation = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Heure d'investigation"
    )
    nom_equipe_investigateur = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Nom de l'équipe/investigateur"
    )

    class Meta:
        verbose_name_plural = "Alertes et Investigations"

    def __str__(self):
        return self.identifiant_alerte if self.identifiant_alerte else super().__str__()

    def save(self, *args, **kwargs):
        # Ajout des contraintes de validation pour chaque champ
        if self.date_notification and self.date_investigation and self.date_notification > self.date_investigation:
            raise ValueError("La date d'investigation ne peut pas être antérieure à la date de notification.")
        super().save(*args, **kwargs)
