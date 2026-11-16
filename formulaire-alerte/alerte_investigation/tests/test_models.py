import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from alerte_investigation.models import AlerteInvestigation, SourceAlerte, valider_telephone


def nouvelle_alerte(**champs):
    valeurs = {
        "identifiant_alerte": "ABC123XYZ",
        "date_notification": datetime.date(2024, 5, 1),
        "heure_alerte": datetime.time(8, 30),
        "source_alerte": SourceAlerte.FOSA,
    }
    valeurs.update(champs)
    return AlerteInvestigation(**valeurs)


class ModeleAlerteTests(TestCase):
    def test_alerte_valide_enregistree(self):
        alerte = nouvelle_alerte()
        alerte.full_clean()
        alerte.save()
        self.assertEqual(AlerteInvestigation.objects.count(), 1)
        self.assertEqual(str(alerte), "ABC123XYZ (01/05/2024)")

    def test_investigation_avant_notification_refusee(self):
        alerte = nouvelle_alerte(date_investigation=datetime.date(2024, 4, 30))
        with self.assertRaises(ValidationError) as contexte:
            alerte.full_clean()
        self.assertIn("date_investigation", contexte.exception.message_dict)

    def test_contrainte_de_dates_en_base(self):
        """Même sans passer par la validation, la base refuse des dates incohérentes."""
        alerte = nouvelle_alerte(date_investigation=datetime.date(2024, 4, 30))
        with self.assertRaises(IntegrityError), transaction.atomic():
            alerte.save()

    def test_meme_jour_accepte(self):
        nouvelle_alerte(date_investigation=datetime.date(2024, 5, 1)).full_clean()

    def test_source_autre_exige_une_precision(self):
        with self.assertRaises(ValidationError) as contexte:
            nouvelle_alerte(source_alerte=SourceAlerte.AUTRE).full_clean()
        self.assertIn("source_alerte_precision", contexte.exception.message_dict)
        nouvelle_alerte(source_alerte=SourceAlerte.AUTRE, source_alerte_precision="Média local").full_clean()

    def test_identifiant_unique(self):
        nouvelle_alerte().save()
        with self.assertRaises(ValidationError) as contexte:
            nouvelle_alerte().full_clean()
        self.assertIn("identifiant_alerte", contexte.exception.message_dict)

    def test_identifiant_de_9_caracteres_alphanumeriques(self):
        for identifiant in ("ABC123XY", "ABC123XYZ0", "ABC-23XYZ"):
            with self.subTest(identifiant=identifiant), self.assertRaises(ValidationError):
                nouvelle_alerte(identifiant_alerte=identifiant).full_clean()


class ValidationTelephoneTests(TestCase):
    def test_numeros_acceptes(self):
        for numero in ("0612345", "+33 6 12 34 56 78", "(022) 123-45-67", "699.99.99.99"):
            with self.subTest(numero=numero):
                valider_telephone(numero)

    def test_numeros_refuses(self):
        for numero in ("abcdefg", "123456", "06 12 34 ab", "1234567890123456", "12+34567"):
            with self.subTest(numero=numero), self.assertRaises(ValidationError):
                valider_telephone(numero)
