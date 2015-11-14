from django.db import models
from pysimplesoap.client import SoapClient

# Provides an api to get multiple kinds of data.
# These can be accessed by the functions below.
# Where there can be no base currency provided, the EUR is set as the base currency.
kowabunga_sc = SoapClient(wsdl='http://currencyconverter.kowabunga.net/converter.asmx?WSDL')

# Provides only conversion rates between 2 currencies.
# It is not possible to get rates from the past or do direct calculations.
webservicex_sc = SoapClient(wsdl='http://www.webservicex.net/currencyconvertor.asmx?WSDL')


def get_currencies():
    """
    :return: A list of all the currencies from http://currencyconverter.kowabunga.net/converter.asmx?WSDL
    """
    currencies = kowabunga_sc.GetCurrencies()
    return currencies


def get_currency_rate(currency, date):
    """
    :param currency: The counter currency.
    :param date: The date the currency has to be calculated on.
    :return: The currency rate on the specified date, with the "EUR" as base currency.
    """
    currency_rate = kowabunga_sc.GetCurrencyRate(Currency=currency, RateDate=date)
    currency_rate = currency_rate["GetCurrencyRateResult"]
    currency_rate = round(float(currency_rate), 4)
    return currency_rate


def get_conversion_rate(currency_from, currency_to, date):
    """
    Calculate the conversion rate between 2 currencies
    :param currency_from: The base currency
    :param currency_to: The counter currency
    :param date: The date the conversion rate has to be calculated on
    :return: The conversion rate of the 2 currencies on the specified date.
    """
    conversion_rate = kowabunga_sc.GetConversionRate(CurrencyFrom=currency_from, CurrencyTo=currency_to,
                                                     RateDate=date)
    conversion_rate = conversion_rate["GetConversionRateResult"]
    if conversion_rate == 0:
        conversion_rate = webservicex_sc.ConversionRate(FromCurrency=currency_from, ToCurrency=currency_to)
        conversion_rate = conversion_rate["ConversionRateResult"]
    conversion_rate = round(float(conversion_rate), 4)
    return conversion_rate


def get_conversion_amount(currency_from, currency_to, date, amount):
    """
    Calculate the counter currency amount based on the base currency, base currency amount and the date.
    :param currency_from: The base currency
    :param currency_to: The counter currency
    :param date: The date the amount has to be converted on
    :param amount: The base currency amount
    :return: The counter currency amount
    """
    conversion_rate = get_conversion_rate(currency_from, currency_to, date)
    conversion_amount = float(conversion_rate) * float(amount)
    conversion_amount = round(conversion_amount, 4)

    return conversion_amount


class Currency(models.Model):
    """
    Base class for currencies.
    """
    currency_name = models.CharField(max_length=50, null=False, blank=False)
    currency_code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.currency_code

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class CurrencyPair(models.Model):
    """
    Base class for storing currency pairs.
    """
    base_currency = models.ForeignKey('Currency', to_field='currency_code', related_name='base_currency')
    counter_currency = models.ForeignKey('Currency', to_field='currency_code', related_name='counter_currency')
    default_show = models.BooleanField(help_text='Toon dit currencypair op de website.', default=False,
                                       verbose_name='Toon')

    def calculate_currency_pair(self, date):
        """
        :param date: The date the rate of the currency pair has to be calculated on.
        :return: The rate  between the base and the counter currency on the specified date.
        """
        currency_pair_rate = get_conversion_rate(self.base_currency.currency_code,
                                                 self.counter_currency.currency_code, date)
        return currency_pair_rate

    class Meta:
        verbose_name = "Currency pair"
        verbose_name_plural = "Currency pairs"


class CurrencyPairHistory(models.Model):
    """
    Store currency pair rates in the database for every requested date.
    This prevents the site to pull a request from the SOAP server every time.
    This will make te site faster.
    """
    currency_pair = models.ForeignKey('CurrencyPair')
    date = models.DateField()
    currency_pair_rate = models.FloatField()

    @staticmethod
    def get_or_create(currency_pair, date):
        """
        Check if the currency pair on the selected date already exists in the database, else create a new entry.
        :param currency_pair: The currency pair
        :param date: The date for the requested currency pair rate
        :return: Existing or new entry for a CurrencyPairHistory instance.
        """
        obj = CurrencyPairHistory()
        try:
            obj = CurrencyPairHistory.objects.get(currency_pair=currency_pair, date=date)
        except CurrencyPairHistory.DoesNotExist:
            obj = CurrencyPairHistory()
            obj.currency_pair = currency_pair
            obj.date = date
            obj.currency_pair_rate = get_conversion_rate(currency_pair.base_currency_id,
                                                         currency_pair.counter_currency_id, date)
            obj.save()
        finally:
            return obj
