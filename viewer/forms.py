from django import forms
from viewer.models import Bid

from viewer.models import AddAuction
from viewer.models import AddAuction, UserAccounts, AccountType
from django.forms import ModelForm
from django.forms import (
  CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea, SelectDateWidget
)
import re
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.db.transaction import atomic
from django.forms import CharField, Form, Textarea, EmailField, ModelForm
from viewer.models import Profile, AccountStatus, AccountType
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    city = forms.CharField(max_length=128, required=True)
    address = forms.CharField(max_length=256, required=True)
    zip_code = forms.CharField(max_length=10, required=True)
    avatar = forms.ImageField(required=False)
    account_type = forms.ModelChoiceField(queryset=AccountType.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'city', 'address', 'zip_code', 'avatar', 'account_type')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Uživatel s tímto uživatelským jménem již existuje.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        print(f"DEBUG: Username being saved: {user.username}")  # Zobrazí uživatelské jméno
        if commit:
            user.save()
            print(f"DEBUG: User {user.username} saved successfully.")

            # Přidej profil
            profile = Profile.objects.create(
                user=user,
                city=self.cleaned_data['city'],
                address=self.cleaned_data['address'],
                zip_code=self.cleaned_data['zip_code'],
                avatar=self.cleaned_data['avatar']
            )

            # Uložení typu účtu
            account_type = self.cleaned_data['account_type']
            UserAccounts.objects.create(user=user, account_type=account_type)

        return user

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccounts
        fields = ['account_type']

    account_type = forms.ModelChoiceField(queryset=AccountType.objects.all(), empty_label="Vyberte typ účtu")

class AddAuctionForm(ModelForm):
    class Meta:
        model = AddAuction
        fields = '__all__'  # Zahrnuje všechna pole
        widgets = {
            'price': forms.HiddenInput(),
            'previous_price': forms.HiddenInput(),
            'number_of_views': forms.HiddenInput(),
            'promotion': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AddAuctionForm, self).__init__(*args, **kwargs)
        # Zajištění, že pole 'user_creater', 'name_bider', a 'name_buyer' nejsou zahrnuta ve formuláři
        self.fields.pop('user_creater')  # Odebere pole 'user_creater' z formuláře
        self.fields.pop('name_bider')  # Odebere pole 'name_bider' z formuláře
        self.fields.pop('name_buyer')



from django import forms
from .models import Bid

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Bid amount must be greater than 0.")
        return amount

from django import forms
from .models import AddAuction, Category

class AuctionSearchForm(forms.Form):
    name_auction = forms.CharField(required=False, label='Název aukce', max_length=128)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Kategorie')

    # Zde přímo přidáme volby
    AUCTION_TYPE_CHOICES = [('buy_now', 'Buy Now'), ('place_bid', 'Place Bid')]
    auction_type = forms.ChoiceField(choices=AUCTION_TYPE_CHOICES, required=False, label='Typ aukce')

    price_from = forms.DecimalField(required=False, label='Cena od', max_digits=10, decimal_places=2)
    price_to = forms.DecimalField(required=False, label='Cena do', max_digits=10, decimal_places=2)
    auction_start_date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Datum začátku od')
    auction_start_date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Datum začátku do')








# PŘETÁHNUTO Z HOLLYMOVIES
# class MovieForm(ModelForm):
#
#   class Meta:
#     model = Movie
#     fields = '__all__'
#
#   #title = CharField(validators=[capitalized_validator])
#   #rating = IntegerField(min_value=1, max_value=10)
#   #released = PastMonthField()
#
#   def clean_description(self):
#     # Každá věta bude začínat velkým písmenem
#     initial = self.cleaned_data['description']
#     sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
#     return '. '.join(sentence.capitalize() for sentence in sentences)
#
#   def clean(self):
#     result = super().clean()
#     if result['genre'].name == 'commedy' and result['rating'] > 5:
#       raise ValidationError(
#         "Commedies aren't so good to be rated over 5."
#       )
#     return result