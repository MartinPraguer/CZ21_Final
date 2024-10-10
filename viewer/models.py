from django.db import models
from django.db.models import Model, DO_NOTHING, CharField, DateField, ForeignKey, IntegerField, TextField, BooleanField, ImageField, DateTimeField
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import CASCADE, Model, OneToOneField, TextField


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    biography = TextField()



# from django.forms import


# jaký je rozdíl mezi db.models a forms Charfield

class AccountStatus(Model): #aktivní/neaktivní/blokovaný
    account_status = CharField(max_length=128)

    def __str__(self):
        return f"status účtu: {self.account_status}"

class AccountType(Model): #běžný/prémium
    account_type = CharField(max_length=128)

    def __str__(self):
        return f"typ účtu: {self.account_type}"

class UserAccounts(Model):
    pass
    '''
    email = CharField(max_length=128)
    password = CharField(max_length=128)
    nickname = CharField(max_length=128)
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    city = CharField(max_length=128)
    address = CharField(max_length=128)
    house_number = CharField(max_length=128)
    zip_code = CharField(max_length=128)
    created = DateTimeField(auto_now_add=True)
    account_status = ForeignKey(AccountStatus, on_delete=DO_NOTHING) #aktivní/neaktivní/blokovaný
    # avatar = odkaz na jpg/gif
    account_type = ForeignKey(AccountType, on_delete=DO_NOTHING) #běžný/prémium

    def __str__(self):
        return f"{self.nickname}"
'''
class Category(Model):
    name = CharField(max_length=128)



    def __str__(self):
        return f"{self.name}"

class Auction(Model):
    name = CharField(max_length=128)
    category = ForeignKey('Category', on_delete=models.CASCADE, default=1)  # Opravený řetězcový odkaz na Category
    description = TextField(default="No description provided")
    photo =  ImageField(upload_to='photos/', null=True, blank=True)
    minimum_bid = IntegerField(default=0)
    # maximum_bid = IntegerField(default=0)
    price = IntegerField(default=0)
    buy_now = BooleanField(default=False)
    promotion = BooleanField(default=False)
    auction_start_date = DateTimeField(default=datetime.now)
    auction_end_date = DateTimeField(default=datetime.now)
    number_of_views = IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.category} - {self.description}"


class TransactionEvalution(Model):
    auction = ForeignKey(Auction, on_delete=DO_NOTHING)
    seller_rating = IntegerField()
    sellers_comment = TextField()
    buyer_rating = IntegerField()
    buyers_comment = TextField()

    def __str__(self):
        return f"{self.auction} - {self.sell_rating} - {self.buyer_rating}"

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db import models

class AddAuction(Model):
    name = CharField(max_length=128)
    user = ForeignKey(User, on_delete=models.DO_NOTHING)
    category = ForeignKey(Category, on_delete=models.DO_NOTHING)
    description = TextField()
    photo = models.ImageField(upload_to='photos/')
    minimum_bid = IntegerField(default=0)
    # maximum_bid = IntegerField(default=0)
    buy_now = BooleanField(default=False) # !zašknutí políčka buy_now = True!
    promotion = BooleanField(default=False) # !zašknutí políčka promotion = True!
    auction_start_date = DateTimeField(default=datetime.now)
    auction_end_date = DateTimeField(default=datetime.now)
    number_of_views = IntegerField(default=0)
    created = DateTimeField(default=timezone.now)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)



    def __str__(self):
        return f"{self.name} - {self.user} -{self.category} - {self.description}"



from django.db import models
from django.contrib.auth.models import User

class Bid(models.Model):
    add_auction = models.ForeignKey('AddAuction', on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"