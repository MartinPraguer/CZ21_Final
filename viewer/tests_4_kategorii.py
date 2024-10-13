# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import Category, AddAuction
#
# class AuctionTemplateTestCase(TestCase):
#     def setUp(self):
#         # Vytvoříme testovacího uživatele
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#
#         # Vytvoříme 4 kategorie
#         self.Statues = Category.objects.create(name="Statues")
#         self.Paintings = Category.objects.create(name="Paintings")
#         self.Numismatics = Category.objects.create(name="Numismatics")
#         self.Jewelry = Category.objects.create(name="Jewelry")
#
#         # Vytvoříme dynamické aukce
#         self.auction1 = AddAuction.objects.create(
#             name_auction="Unique Auction 1", category=self.category1, price=100, auction_type='place_bid', user_creator=self.user
#         )
#         self.auction2 = AddAuction.objects.create(
#             name_auction="Unique Auction 2", category=self.category1, price=200, auction_type='buy_now', user_creator=self.user
#         )
#
#     def test_category1_template_render(self):
#         response = self.client.get(reverse('category_detail', args=[self.category1.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'template_name.html')
#
#         # Testování dynamického obsahu
#         self.assertContains(response, self.auction1.name_auction)  # Ověřuje, že se objeví název aukce
#         self.assertContains(response, self.auction1.price)  # Ověřuje, že se objeví cena
#         self.assertContains(response, self.auction2.name_auction)  # Druhá aukce
#         self.assertContains(response, self.auction2.price)  # Cena druhé aukce