from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField, ForeignKey, CharField, DateTimeField, IntegerField, TextField, BooleanField, ImageField
from django.utils import timezone
from datetime import timedelta

class AccountStatus(models.Model):
    account_status = CharField(max_length=128)

    def __str__(self):
        return self.account_status

class AccountType(models.Model):
    account_type = CharField(max_length=128)

    def __str__(self):
        return self.account_type

class UserAccounts(models.Model):  # Přidání modelu UserAccounts
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Přidej další pole podle potřeby

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    city = CharField(max_length=128, default="City")
    address = CharField(max_length=256, default="Address")  # Ulice, číslo domu
    zip_code = CharField(max_length=10, default="00000")
    created_at = DateTimeField(auto_now_add=True)
    account_status = OneToOneField(AccountStatus, on_delete=models.SET_NULL, null=True)
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username



class Category(models.Model):
    name = CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"

# class Auction(models.Model):
#     name = CharField(max_length=128)
#     category = ForeignKey(Category, on_delete=models.CASCADE, default=1)  # Opravený řetězcový odkaz na Category
#     description = TextField(default="No description provided")
#     photo = ImageField(upload_to='photos/', null=True, blank=True)
#     minimum_bid = IntegerField(default=0)
#     price = IntegerField(default=0)
#     buy_now = BooleanField(default=False)
#     promotion = BooleanField(default=False)
#     auction_start_date = DateTimeField(auto_now_add=True)
#     auction_end_date = DateTimeField(auto_now_add=True)
#     number_of_views = IntegerField(default=0)

    # def __str__(self):
    #     return f"{self.name} - {self.category} - {self.description}"

# class TransactionEvaluation(models.Model):
#     auction = ForeignKey(Auction, on_delete=models.DO_NOTHING)
#     seller_rating = IntegerField()
#     sellers_comment = TextField()
#     buyer_rating = IntegerField()
#     buyers_comment = TextField()

    # def __str__(self):
    #     return f"{self.auction} - {self.seller_rating} - {self.buyer_rating}"


class AddAuction(models.Model):
    photo = ImageField(upload_to='photos/')
    name_auction = CharField(max_length=128)  # Zde se používá 'name_auction'
    user_creator = ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_auctions')
    name_bider = ForeignKey(User, on_delete=models.DO_NOTHING, related_name='bided_auctions', null=True, blank=True)
    name_buyer = ForeignKey(User, on_delete=models.DO_NOTHING, related_name='listed_auctions', null=True, blank=True)
    category = ForeignKey(Category, on_delete=models.DO_NOTHING)

    # Přidání výchozí hodnoty pro popis
    description = TextField(default="No description provided")
    promotion = BooleanField(default=False)  # Toto pole zůstává jako nullable
    auction_start_date = DateTimeField(auto_now_add=True)
    auction_end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Ověření, zda je auction_start_date None, a nastavení na aktuální čas, pokud je None
        if not self.auction_start_date:
            self.auction_start_date = timezone.now()

        # Pokud auction_end_date není nastaveno, přidáme týden k auction_start_date
        if not self.auction_end_date:
            self.auction_end_date = self.auction_start_date + timedelta(weeks=1)

        super().save(*args, **kwargs)


    number_of_views = IntegerField(default=0)
    created = DateTimeField(auto_now_add=True)

    # Typ aukce
    AUCTION_TYPE_CHOICES = [
        ('buy_now', 'Buy Now'),
        ('place_bid', 'Place Bid'),
    ]
    auction_type = models.CharField(
        max_length=10,
        choices=AUCTION_TYPE_CHOICES,
        default='place_bid'
    )

    # "Buy Now" políčka
    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # "Place Bid" políčka
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    minimum_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name_auction} - {self.user_creator} - {self.category} - {self.description}"

class Bid(models.Model):
    auction = models.ForeignKey(AddAuction, related_name='bids', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} Kč"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AddAuction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Přidání metody pro přidání do košíku
    @classmethod
    def add_to_cart(cls, user, auction):
        # Získáme nebo vytvoříme položku v košíku
        cart_item, created = cls.objects.get_or_create(
            user=user,
            auction=auction,
            defaults={'price': auction.buy_now_price}
        )

        if not created:
            # Pokud už existuje, aktualizujeme cenu
            cart_item.price = auction.buy_now_price
            cart_item.save()

        return cart_item