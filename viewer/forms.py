from django import forms
from viewer.models import Bid

from viewer.models import AddAuction
from viewer.models import AddAuction
from django.forms import ModelForm
from django.forms import (
  CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea, SelectDateWidget
)
import re
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.db.transaction import atomic
from django.forms import CharField, Form, Textarea, EmailField
from viewer.models import Profile
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Disable account until it is confirmed via email
        if commit:
            user.save()
        return user

class AddAuctionForm(ModelForm):
    class Meta:
        model = AddAuction
        fields = '__all__'
        widgets = {
            'penultimate_price': forms.HiddenInput(),
            'last_price': forms.HiddenInput(),
            'number_of_views': forms.HiddenInput(),
            'promotion': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AddAuctionForm, self).__init__(*args, **kwargs)
        # Zajištění, že pole user není zahrnuto ve formuláři
        self.fields.pop('user')  # Odebere pole 'user' z formuláře, aby nebylo zobrazeno

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