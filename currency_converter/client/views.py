from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from client.models import get_conversion_amount, CurrencyPairHistory, CurrencyPair
from client.forms import CurrencyConverterForm, LoginForm, RegistrationForm


def index(request):
    if 'login' in request.POST:
        login_form = LoginForm(request.POST)
        registration_form = RegistrationForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                message = "U bent ingelogd"
            else:
                message = "Uw account is niet meer actief!\nNeem contact op met de beheerder."
        else:
            message = "Er is iets mis gegaan. Probeer het opnieuw."

    elif 'register' in request.POST:
        registration_form = RegistrationForm(request.POST)
        login_form = LoginForm()
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            message = "Het wachtwoord moet in beide velden identiek zijn!"
        else:
            user = User.objects.create_user(username, email, password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            message = "Uw account is aangemaakt en u bent ingelogd."

    elif 'logout' in request.POST:
        login_form = LoginForm()
        registration_form = RegistrationForm()
        logout(request)
        message = "U bent uitgelogd."

    else:
        login_form = LoginForm()
        registration_form = RegistrationForm()
        message = "Voer uw gegevens in om in te loggen."

    context = {
        'login_form': login_form,
        'registration_form': registration_form,
        'message': message,
    }
    return render(request, '../templates/index.html', context)


@login_required
def currency_converter(request):
    counter_amount = ""
    if request.GET:
        form = CurrencyConverterForm(request.GET)
        if form.is_valid():
            # Get the input data from the form
            base_currency = form.cleaned_data['base_currency']
            counter_currency = form.cleaned_data['counter_currency']
            base_amount = form.cleaned_data['base_amount']

            # Calculate the counter_amount
            counter_amount = get_conversion_amount(base_currency, counter_currency, datetime.now(), base_amount)

    else:
        form = CurrencyConverterForm()

    context = {
        'form': form,
        'counter_amount': counter_amount
    }

    return render(request, '../templates/client/currencyconverter.html', context)


@login_required
def currency_rates(request):
    currency_pairs_values = []
    currency_pairs = CurrencyPair.objects.filter(default_show=True)
    for currency_pair in currency_pairs:
        currency_pair_value = CurrencyPairHistory.get_or_create(currency_pair, datetime.now())
        currency_pairs_values.append(currency_pair_value)

    if request.GET:
        currency_pair_id = request.GET.get('id')
        today = datetime.now()

        # get todays currency_pairs_values
        current_currency_pair = CurrencyPair.objects.get(pk=currency_pair_id)

        historic_values = []
        currency_pair = CurrencyPair.objects.get(pk=currency_pair_id)
        days = 60
        while days > 0:
            date = today - timedelta(days=days)
            currency_pair_value = CurrencyPairHistory.get_or_create(currency_pair, date)
            historic_values.append(currency_pair_value)
            days -= 1

        context = {
            'currency_pairs_values': currency_pairs_values,
            'historic_values': historic_values,
            'current_currency_pair': current_currency_pair,
        }

    else:
        context = {
            'currency_pairs_values': currency_pairs_values,
        }

    return render(request, '../templates/client/currencypairs.html', context)
