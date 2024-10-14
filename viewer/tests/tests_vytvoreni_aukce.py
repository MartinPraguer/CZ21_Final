from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from viewer.models import AddAuction, Category
import os
from django.core.files.uploadedfile import SimpleUploadedFile

class CreateAuctionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.statues_category = Category.objects.create(name="Statues")
        self.paintings_category = Category.objects.create(name="Paintings")
        self.numismatics_category = Category.objects.create(name="Numismatics")
        self.jewelry_category = Category.objects.create(name="Jewelry")

        # Cesta ke skutečnému GIF obrázku
        self.image_path = os.path.join(os.path.dirname(__file__), 'test_image.gif')

    def create_auction(self, category, auction_type):
        self.client.login(username='testuser', password='testpass')

        # Otevřeme skutečný testovací obrázek GIF
        with open(self.image_path, 'rb') as img:
            image = SimpleUploadedFile("test_image.gif", img.read(), content_type="image/gif")

            # Data, která budeme odesílat ve formuláři
            form_data = {
                'name_auction': f'Test Auction for {category.name} - {auction_type}',
                'category': category.id,
                'auction_type': auction_type,
                'start_price': 50.00,
                'minimum_bid': 10.00,
                'description': f'This is a test auction for {category.name} with {auction_type} type.',
                'photo': image,
                'number_of_views': 0  # Přidáme number_of_views do formuláře
            }

            if auction_type == 'buy_now':
                form_data['buy_now_price'] = 100.00  # Přidáme buy_now cenu, pokud je typ aukce "buy_now"

            # Odeslání POST požadavku na URL pro vytvoření aukce
            response = self.client.post(reverse('add_auction_create'), form_data)

            if response.status_code == 200:
                print(response.context['form'].errors)

            # Ověříme, že došlo k přesměrování po úspěšném vytvoření (status code 302)
            self.assertEqual(response.status_code, 302)

            # Ověříme, že aukce byla vytvořena v databázi
            auction = AddAuction.objects.get(name_auction=form_data['name_auction'])
            self.assertEqual(auction.category, category)
            self.assertEqual(auction.auction_type, auction_type)
            self.assertEqual(auction.user_creator, self.user)
            if auction_type == 'buy_now':
                self.assertEqual(auction.buy_now_price, 100.00)

    # Testy pro jednotlivé kategorie a typy aukcí

    def test_create_statues_place_bid_auction(self):
        self.create_auction(self.statues_category, 'place_bid')

    def test_create_statues_buy_now_auction(self):
        self.create_auction(self.statues_category, 'buy_now')

    def test_create_paintings_place_bid_auction(self):
        self.create_auction(self.paintings_category, 'place_bid')

    def test_create_paintings_buy_now_auction(self):
        self.create_auction(self.paintings_category, 'buy_now')

    def test_create_numismatics_place_bid_auction(self):
        self.create_auction(self.numismatics_category, 'place_bid')

    def test_create_numismatics_buy_now_auction(self):
        self.create_auction(self.numismatics_category, 'buy_now')

    def test_create_jewelry_place_bid_auction(self):
        self.create_auction(self.jewelry_category, 'place_bid')

    def test_create_jewelry_buy_now_auction(self):
        self.create_auction(self.jewelry_category, 'buy_now')