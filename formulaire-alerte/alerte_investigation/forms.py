"""Formulaire de saisie d'une alerte et de son investigation."""

from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Fieldset, Layout, Row, Submit
from django import forms

from .models import AlerteInvestigation


def _date():
    return forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")


def _heure():
    return forms.TimeInput(attrs={"type": "time"}, format="%H:%M")


class AlerteInvestigationForm(forms.ModelForm):
    """Saisie d'une alerte ; la mise en page est décrite par ``self.helper`` (crispy-forms)."""

    class Meta:
        model = AlerteInvestigation
        fields = [
            "identifiant_alerte",
            "date_notification",
            "heure_alerte",
            "personne_structure_transmis_alerte",
            "numero_telephone",
            "source_alerte",
            "source_alerte_precision",
            "heure_information_equipe",
            "heure_arrivee_site",
            "date_investigation",
            "heure_investigation",
            "nom_equipe_investigateur",
        ]
        widgets = {
            "identifiant_alerte": forms.TextInput(
                attrs={
                    "pattern": "[A-Za-z0-9]{9}",
                    "title": "9 caractères alphanumériques",
                    "autocomplete": "off",
                }
            ),
            "numero_telephone": forms.TextInput(attrs={"type": "tel", "autocomplete": "tel"}),
            "source_alerte": forms.RadioSelect,
            "date_notification": _date(),
            "date_investigation": _date(),
            "heure_alerte": _heure(),
            "heure_information_equipe": _heure(),
            "heure_arrivee_site": _heure(),
            "heure_investigation": _heure(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sans valeur vide proposée : la source est obligatoire.
        self.fields["source_alerte"].choices = [
            choix for choix in self.fields["source_alerte"].choices if choix[0]
        ]

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_id = "formulaire-alerte"
        self.helper.attrs = {"novalidate": ""}  # la validation de référence est côté serveur
        self.helper.layout = Layout(
            Fieldset(
                "Alerte",
                Row(
                    Column("identifiant_alerte", css_class="col-md-4"),
                    Column("date_notification", css_class="col-md-4"),
                    Column("heure_alerte", css_class="col-md-4"),
                ),
                Row(
                    Column("personne_structure_transmis_alerte", css_class="col-md-8"),
                    Column("numero_telephone", css_class="col-md-4"),
                ),
                InlineRadios("source_alerte"),
                Div("source_alerte_precision", css_id="bloc-precision-source"),
            ),
            Fieldset(
                "Investigation",
                Row(
                    Column("heure_information_equipe", css_class="col-md-6"),
                    Column("heure_arrivee_site", css_class="col-md-6"),
                ),
                Row(
                    Column("date_investigation", css_class="col-md-6"),
                    Column("heure_investigation", css_class="col-md-6"),
                ),
                "nom_equipe_investigateur",
            ),
            Submit("enregistrer", "Enregistrer l'alerte", css_class="btn-primary"),
        )
