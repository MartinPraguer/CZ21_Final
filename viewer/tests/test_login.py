from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginTest(TestCase):
    def setUp(self):
        # Vytvoříme testovacího uživatele
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_with_valid_credentials(self):
        # Přihlašovací URL
        login_url = reverse('login')

        # Odeslání platných přihlašovacích údajů
        response = self.client.post(login_url, {
            'username': self.username,
            'password': self.password,
        })

        # Zkontroluj přesměrování po úspěšném přihlášení
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))  # Zde se přesměruje na stránku po přihlášení (např. home)

    def test_login_with_invalid_credentials(self):
        # Přihlašovací URL
        login_url = reverse('login')

        # Odeslání nesprávných přihlašovacích údajů
        response = self.client.post(login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword',
        })

        # Zkontroluj, že přihlášení neproběhlo
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')
