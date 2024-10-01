from django.db import models
from django.db.models import Model, DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField, TextField, BooleanField
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
        return f"categorie - {self.name}"

class Auction(Model):
    name = CharField(max_length=128)
    '''
    category = ForeignKey(Category, on_delete=DO_NOTHING)
    description = TextField()
    # fotky
    minimum_bid = IntegerField()
    maximum_bid = IntegerField()
    price = IntegerField()
    buy_now = BooleanField(default=False)
    promotion = BooleanField(default=False)
    auction_start_date = DateField()
    auction_end_date = DateField()
    number_of_views = IntegerField()
    

    def __str__(self):
        return f"{self.name} - {self.category} - {self.description}"
    '''

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

class Advertisement(Model):
    name = CharField(max_length=128)
    user = ForeignKey(User, on_delete=DO_NOTHING)
    category = ForeignKey(Category, on_delete=DO_NOTHING)
    description = TextField()

    def __str__(self):
        return f"{self.name} - {self.user} -{self.category} - {self.description}"