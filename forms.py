from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from crispy_forms.bootstrap import PrependedText
from widget_caseacocher import CustomCheckbox
from .models import AlerteInvestigation

class AlerteInvestigationForm(forms.ModelForm):
    """
    Formulaire pour les alertes et les investigations.
    """
    class Meta:
        model = AlerteInvestigation
        fields = [
            'identifiant_alerte', 'date_notification', 'numero_telephone', 'heure_alerte', 'personne_structure_transmis_alerte', 
            'source_alerte', 'heure_information_equipe', 'heure_arrivee_site', 'date_investigation', 
            'heure_investigation', 'nom_equipe_investigateur',
        ]
        widgets = {
            'date_notification': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_alerte': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'source_alerte': CustomCheckbox(attrs={'class': 'form-control'}, hidden_fields_mapping={
                "Centre d'appel": "centre_appel",
                "Suivi des contacts": "suivi_contacts",
                "EIIR": "eiir",
                "Point d'entrée": "point_entree",
                "ASC": "asc",
                "Communauté": "communaute",
                "FOSA": "fosa",
                "Autre": "autre"
            }),
            'heure_information_equipe': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'heure_arrivee_site': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'date_investigation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_investigation': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire avec un layout crispy et des champs personnalisés.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Alerte et Investigation',
                PrependedText('identifiant_alerte', '', placeholder='ID Alerte'),
                'date_notification',
                PrependedText('numero_telephone', '', placeholder='N°Tél', attrs={'minlength': '9'}),
                'heure_alerte',
                PrependedText('personne_structure_transmis_alerte', '', placeholder="Personne (ou structure) ayant transmis l'alerte"),
                'source_alerte',
                'heure_information_equipe',
                'heure_arrivee_site',
                'date_investigation',
                'heure_investigation',
                PrependedText('nom_equipe_investigateur', '', placeholder="Nom de l'équipe/investigateur")
            ),
        )
