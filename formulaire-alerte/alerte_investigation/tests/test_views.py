from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from alerte_investigation.models import AlerteInvestigation

from .factories import donnees


class VueSaisieTests(TestCase):
    url = reverse("alerte_investigation:saisie")

    def test_affichage(self):
        reponse = self.client.get(self.url)
        self.assertEqual(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, "alerte_investigation/alerte_form.html")
        self.assertContains(reponse, 'id="formulaire-alerte"')
        self.assertContains(reponse, 'type="radio"', count=8)
        self.assertContains(reponse, "csrfmiddlewaretoken")

    def test_html_bien_forme(self):
        """Autant de <div> ouvrants que fermants dans la page rendue."""
        html = self.client.get(self.url).content.decode()
        self.assertEqual(html.count("<div"), html.count("</div>"))

    def test_enregistrement_puis_redirection(self):
        reponse = self.client.post(self.url, donnees(), follow=True)
        self.assertRedirects(reponse, self.url)
        self.assertEqual(AlerteInvestigation.objects.count(), 1)
        self.assertContains(reponse, "L&#x27;alerte ABC123XYZ a bien été enregistrée.")

    def test_donnees_invalides_reaffichees_sans_erreur_serveur(self):
        reponse = self.client.post(
            self.url, donnees(date_notification="2024-05-10", date_investigation="2024-05-02")
        )
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "ne peut pas être antérieure")
        self.assertEqual(AlerteInvestigation.objects.count(), 0)

    def test_identifiant_en_double(self):
        self.client.post(self.url, donnees())
        reponse = self.client.post(self.url, donnees())
        self.assertContains(reponse, "Une alerte avec cet identifiant existe déjà.")
        self.assertEqual(AlerteInvestigation.objects.count(), 1)


class AdministrationTests(TestCase):
    def test_liste_des_alertes_dans_l_admin(self):
        admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "x")
        self.client.force_login(admin)
        self.client.post(reverse("alerte_investigation:saisie"), donnees())
        reponse = self.client.get(reverse("admin:alerte_investigation_alerteinvestigation_changelist"))
        self.assertContains(reponse, "ABC123XYZ")
