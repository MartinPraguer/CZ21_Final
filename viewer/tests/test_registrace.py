from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationTest(TestCase):
    def test_registration_with_valid_data(self):
        # URL pro registraci
        register_url = reverse('sign_up')  # Ujisti se, že máš tuto URL definovanou v urls.py

        # Data, která budeš posílat pro registraci
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'city': 'Test City',
            'address': '123 Test Street',
            'zip_code': '12345',
            'account_type': 1,  # nebo jakýkoliv jiný typ účtu
            # Můžeš přidat další pole podle svého formuláře
        }

        # Odeslání POST požadavku s daty
        response = self.client.post(register_url, data)

        # Ověření, zda registrace proběhla úspěšně
        self.assertEqual(response.status_code, 302)  # 302 znamená přesměrování po úspěšné registraci
        self.assertRedirects(response, reverse('index'))  # Zde se přesměruje na stránku po přihlášení (např. home)
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Ověř, že uživatel byl vytvořen

    def test_registration_with_invalid_data(self):
        # URL pro registraci
        register_url = reverse('sign_up')

        # Data, která jsou neplatná (hesla se neshodují)
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'wrongpassword',
            'city': 'Test City',
            'address': '123 Test Street',
            'zip_code': '12345',
            'account_type': 'User',
        }

        # Odeslání POST požadavku s daty
        response = self.client.post(register_url, data)

        print(response.content)

        # Ověření, že registrace neproběhla úspěšně
        self.assertEqual(response.status_code, 200)  # Formulář by se měl vrátit s chybou
        self.assertContains(response, "The two password fields didn’t match.")  # Ověř, že je zobrazena chybová zpráva
        self.assertFalse(User.objects.filter(username='testuser').exists())  # Uživatel by neměl být vytvořen
