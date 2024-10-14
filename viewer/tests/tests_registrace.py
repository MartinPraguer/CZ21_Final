from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserRegistrationTest(TestCase):
    def test_register_new_user(self):
        # Použijeme unikátní uživatelské jméno pro každý test
        form_data = {
            'username': 'newuser123',  # Změněno pro unikátnost
            'password1': 'password123',
            'password2': 'password123',
            'email': 'newuser123@example.com'
        }
        response = self.client.post(reverse('register'), form_data)

        # Očekáváme přesměrování po úspěšné registraci
        self.assertEqual(response.status_code, 302)

        # Ověříme, že nový uživatel byl vytvořen
        user_exists = User.objects.filter(username='newuser123').exists()
        self.assertTrue(user_exists)



