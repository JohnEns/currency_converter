from django.contrib import admin
from client.models import Currency, CurrencyPair


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['currency_code', 'currency_name']


class CurrencyPairAdmin(admin.ModelAdmin):
    list_display = ['base_currency', 'counter_currency', 'default_show']
    list_filter = ['base_currency', 'counter_currency', 'default_show']
    ordering = ['base_currency', 'counter_currency']

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyPair, CurrencyPairAdmin)
