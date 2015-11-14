# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('currency_name', models.CharField(max_length=50)),
                ('currency_code', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyPair',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('base_currency', models.ForeignKey(related_name='base_currency', to_field='currency_code', to='client.Currency')),
                ('counter_currency', models.ForeignKey(related_name='counter_currency', to_field='currency_code', to='client.Currency')),
            ],
        ),
    ]
