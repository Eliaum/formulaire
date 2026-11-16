from django.test import TestCase

from alerte_investigation.forms import AlerteInvestigationForm

from .factories import donnees


class FormulaireAlerteTests(TestCase):
    def test_donnees_valides(self):
        form = AlerteInvestigationForm(data=donnees())
        self.assertTrue(form.is_valid(), form.errors)

    def test_chaque_source_est_acceptee(self):
        sources = [valeur for valeur, _ in AlerteInvestigationForm().fields["source_alerte"].choices]
        self.assertEqual(len(sources), 8)
        for source in sources:
            precision = "Média local" if source == "autre" else ""
            with self.subTest(source=source):
                form = AlerteInvestigationForm(
                    data=donnees(source_alerte=source, source_alerte_precision=precision)
                )
                self.assertTrue(form.is_valid(), form.errors)

    def test_source_inconnue_refusee(self):
        form = AlerteInvestigationForm(data=donnees(source_alerte="True"))
        self.assertIn("source_alerte", form.errors)

    def test_champs_obligatoires(self):
        form = AlerteInvestigationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            set(form.errors),
            {"identifiant_alerte", "date_notification", "heure_alerte", "source_alerte"},
        )

    def test_investigation_facultative(self):
        form = AlerteInvestigationForm(
            data=donnees(
                heure_information_equipe="",
                heure_arrivee_site="",
                date_investigation="",
                heure_investigation="",
                nom_equipe_investigateur="",
            )
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_dates_incoherentes_donnent_une_erreur_de_formulaire(self):
        form = AlerteInvestigationForm(
            data=donnees(date_notification="2024-05-10", date_investigation="2024-05-02")
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(list(form.errors), ["date_investigation"])

    def test_telephone_avec_lettres_refuse(self):
        form = AlerteInvestigationForm(data=donnees(numero_telephone="abcdefg"))
        self.assertIn("numero_telephone", form.errors)

    def test_rendu_des_huit_sources_en_boutons_radio(self):
        html = AlerteInvestigationForm().as_div()
        self.assertEqual(html.count('type="radio"'), 8)
        self.assertIn("Centre d&#x27;appel", html)
