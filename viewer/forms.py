from viewer.models import UserAccounts
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from viewer.models import Profile, AccountType
from django.contrib.auth.models import User
from django import forms
from .models import AddAuction, Category
from .models import Bid
from multiupload.fields import MultiFileField






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
    # Použití MultiFileField pro nahrávání více obrázků
    images = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)  # Limity souborů

    class Meta:
        model = AddAuction
        fields = '__all__'  # Zahrnuje všechna pole z modelu AddAuction
        widgets = {
            'price': forms.HiddenInput(),
            'previous_price': forms.HiddenInput(),
            'number_of_views': forms.HiddenInput(),
            'promotion': forms.HiddenInput(),
            'auction_end_date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AddAuctionForm, self).__init__(*args, **kwargs)
        # Zajištění, že pole 'user_creator', 'name_bider', a 'name_buyer' nejsou zahrnuta ve formuláři
        self.fields.pop('user_creator')  # Odebere pole 'user_creator' z formuláře
        self.fields.pop('name_bider')  # Odebere pole 'name_bider' z formuláře
        self.fields.pop('name_buyer')  # Odebere pole 'name_buyer' z formuláře


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
