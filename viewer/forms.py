from django import forms

from viewer.models import Add_auction
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
    model = Add_auction
    fields = '__all__'



























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