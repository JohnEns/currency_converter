from django.db import models
from pysimplesoap.client import SoapClient
from datetime import datetime

kowabunga_sc = SoapClient(wsdl='http://currencyconverter.kowabunga.net/converter.asmx?WSDL')


def get_currencies():
    currencies = kowabunga_sc.GetCurrencies()
    return currencies


def get_currency_rate(currency):
    currency_rate = kowabunga_sc.GetCurrencyRate(Currency=currency, RateDate=datetime.now())
    return currency_rate


def get_conversion_rate(currency_from, currency_to):
    conversion_rate = kowabunga_sc.GetConversionRate(CurrencyFrom=currency_from, CurrencyTo=currency_to,
                                                     RateDate=datetime.now())
    return conversion_rate


def get_conversion_amount(currency_from, currency_to, amount):
    conversion_amount = kowabunga_sc.GetConversionAmount(CurrencyFrom=currency_from, CurrencyTo=currency_to,
                                                         RateDate=datetime.now(), Amount=amount)
    return conversion_amount


class CurrencyPair(models.Model):
    base_currency = models.CharField(max_length=3, null=False, blank=False)
    counter_currency = models.CharField(max_length=3, null=False, blank=False)

    def calculate_currency_pair(self):
        currency_pair_rate = get_conversion_rate(self.base_currency, self.counter_currency)
        return currency_pair_rate
