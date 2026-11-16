"""Données de test partagées."""

DONNEES_VALIDES = {
    "identifiant_alerte": "ABC123XYZ",
    "date_notification": "2024-05-01",
    "heure_alerte": "08:30",
    "personne_structure_transmis_alerte": "Centre de santé de quartier",
    "numero_telephone": "+33 6 12 34 56 78",
    "source_alerte": "fosa",
    "source_alerte_precision": "",
    "heure_information_equipe": "09:00",
    "heure_arrivee_site": "10:15",
    "date_investigation": "2024-05-01",
    "heure_investigation": "10:30",
    "nom_equipe_investigateur": "Équipe 1",
}


def donnees(**modifications):
    """Copie des données valides, avec les modifications demandées."""
    return {**DONNEES_VALIDES, **modifications}
