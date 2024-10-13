from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from viewer.models import AccountType

class UserRegistrationTest(TestCase):

    def setUp(self):
        # Vytvoříme instanci AccountType s použitím správného pole 'account_type'
        self.account_type = AccountType.objects.create(account_type="User")

    def test_register_new_user(self):
        # Simulace odeslání formuláře pro registraci nového uživatele
        response = self.client.post(reverse('sign_up'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SuperSecretPassword123',
            'password2': 'SuperSecretPassword123',
            'city': 'Test City',
            'address': 'Test Address',
            'zip_code': '12345',
            'account_type': self.account_type.id,  # Musíme poslat ID typu účtu
        })

        # Pokud formulář není validní, zobrazíme chyby
        if response.status_code == 200:
            print(response.context['form'].errors)  # Zobrazí chyby ve formuláři

        # Ověření, že uživatel byl přesměrován (např. na přihlašovací stránku)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Ověření, že byl vytvořen nový uživatel v databázi
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)



