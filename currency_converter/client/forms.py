from django import forms
from client.models import Currency, CurrencyPair


class CurrencyConverterForm(forms.Form):
    """
    Form input fields for currency converter.
    """
    base_currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    counter_currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    base_amount = forms.FloatField(required=True)


class LoginForm(forms.Form):
    """
    Form input fields for user login.
    """
    username = forms.CharField(min_length=10)
    password = forms.CharField(min_length=10, max_length=32, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    """
    Form input fields for user registration.
    """
    username = forms.CharField(min_length=10, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=10, max_length=32, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(min_length=10, max_length=32, widget=forms.PasswordInput, required=True)
