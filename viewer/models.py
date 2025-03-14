from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField, ForeignKey, CharField, DateTimeField, IntegerField, TextField, BooleanField, \
    ImageField
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum


class AccountStatus(models.Model):
    account_status = CharField(max_length=128)

    def __str__(self):
        return self.account_status


class AccountType(models.Model):
    account_type = models.CharField(max_length=128)

    def __str__(self):
        return self.account_type


class UserAccounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)
    premium_expiry_date = models.DateField(null=True, blank=True)
    purchase_count = models.PositiveIntegerField(default=0)  # Nové pole pro počet nákupů

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"

    # Kontrola, zda je předplatné stále aktivní
    def check_premium_status(self):
        if self.premium_expiry_date and self.premium_expiry_date > timezone.now():
            return True
        return False

    # Nastavení prémiového účtu na jeden měsíc
    def set_premium_subscription(self):
        self.premium_expiry_date = timezone.now() + timedelta(days=30)
        self.is_premium = True
        self.save()


class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    city = CharField(max_length=128, default="City")
    address = CharField(max_length=256, default="Address")  # Ulice, číslo domu
    zip_code = IntegerField(default=00000)
    created_at = DateTimeField(auto_now_add=True)
    account_status = OneToOneField(AccountStatus, on_delete=models.SET_NULL, null=True)
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


from django.db import models
from django.contrib.auth.models import User


class AddAuction(models.Model):
    name_auction = models.CharField(max_length=128)
    user_creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_auctions')
    name_bider = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='bided_auctions', null=True,
                                   blank=True)
    name_buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='listed_auctions', null=True,
                                   blank=True)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    description = models.TextField(default="No description provided")
    promotion = models.BooleanField(default=False)

    auction_start_date = models.DateTimeField(null=True, blank=True)
    # auction_end_date = models.DateTimeField(null=True, blank=True)

    auction_end_date = models.DateTimeField(null=True, blank=True, default=timezone.now() + timedelta(days=7))

    number_of_views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    AUCTION_TYPE_CHOICES = [
        ('buy_now', 'Buy Now'),
        ('place_bid', 'Place Bid'),
    ]
    auction_type = models.CharField(max_length=10, choices=AUCTION_TYPE_CHOICES, default='place_bid')

    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    minimum_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_sold = models.BooleanField(default=False)

    def is_expired(self):
        return self.auction_end_date and self.auction_end_date <= timezone.now()

    def has_bids(self):
        return self.bids.exists()

    def check_is_sold(self):
        if self.auction_type == 'buy_now':
            return self.is_expired() and self.name_buyer is not None
        if self.auction_type == 'place_bid':
            return self.is_expired() and self.has_bids()
        return False

    # DĚLALO CHYBY - ZBOŽÍ SE NEPŘESOUVALO DO KOŠÍKU
    # def save(self, *args, **kwargs):
    #     # Nastavíme datum začátku aukce na aktuální čas, pokud není nastavené
    #     if not self.auction_start_date:
    #         self.auction_start_date = timezone.now()
    #
    #     # Automaticky nastavíme datum konce aukce na 7 dní po začátku
    #     self.auction_end_date = self.auction_start_date + timedelta(days=7)
    #
    #     # Nejprve uložíme aukci, aby měla primární klíč (ID)
    #     super().save(*args, **kwargs)
    #
    #     # Po uložení aukce zkontrolujeme, zda byla prodána, a případně aktualizujeme stav
    #     is_sold_updated = self.check_is_sold()
    #
    #     # Pokud došlo ke změně stavu prodané aukce, znovu ji uložíme
    #     if self.is_sold != is_sold_updated:
    #         self.is_sold = is_sold_updated
    #         super().save(update_fields=['is_sold'])

    def __str__(self):
        return f"{self.name_auction} - {self.user_creator} - {self.category} - {self.description}"



class BuyerEvaluation(models.Model):
    auction = models.ForeignKey(AddAuction, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_rating = models.IntegerField(choices=[(i, f'{i} stars') for i in range(1, 6)], default=5)
    buyer_comment = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction evaluation for auction {self.auction}"

class SellerEvaluation(models.Model):
    auction = models.ForeignKey(AddAuction, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_rating = models.IntegerField(choices=[(i, f'{i} stars') for i in range(1, 6)], default=5)
    seller_comment = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction evaluation for auction {self.auction}"


class Bid(models.Model):
    auction = models.ForeignKey(AddAuction, related_name='bids', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Příhoz uživatele
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                blank=True)  # Cena po přičtení tohoto příhozu
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} Kč"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AddAuction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def add_to_cart(cls, user, auction):
        # Pokusíme se najít položku v košíku podle uživatele a aukce
        cart_item, created = cls.objects.get_or_create(
            user=user,
            auction=auction,  # Každá aukce je jedinečná položka, takže přidáváme vždy jedinečnou položku
            defaults={'price': auction.buy_now_price}  # Cena z "Buy Now"
        )

        if not created:
            # Položka už je v košíku, takže nepřidáme znovu
            print(f"Položka {auction.name_auction} je už v košíku uživatele {user.username}.")

        return cart_item

    # toto je navic k puvodnimu Cart
    @classmethod
    def get_cart_total(cls, user):
        total = cls.objects.filter(user=user).aggregate(Sum('price'))['price__sum']
        return total or 0


class AuctionImage(models.Model):
    auction = models.ForeignKey(AddAuction, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='auction_images/')

    def __str__(self):
        return f"Image for {self.auction.name_auction}"


class ArchivedPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AddAuction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archived purchase: {self.auction.name_auction} by {self.user.username}"


class About(models.Model):
    photo = ImageField(upload_to='about/', null=True, blank=True)
    about_user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=128)
    locket1 = models.TextField()
    locket2 = models.TextField()
    locket3 = models.TextField()
    locket4 = models.TextField()
    locket5 = models.TextField()
