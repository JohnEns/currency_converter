# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyPairHistory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('currency_pair_rate', models.FloatField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name_plural': 'Currencies', 'verbose_name': 'Currency'},
        ),
        migrations.AlterModelOptions(
            name='currencypair',
            options={'verbose_name_plural': 'Currency pairs', 'verbose_name': 'Currency pair'},
        ),
        migrations.AddField(
            model_name='currencypair',
            name='default_show',
            field=models.BooleanField(help_text='Toon dit currencypair op de website.', default=False),
        ),
        migrations.AddField(
            model_name='currencypairhistory',
            name='currency_pair',
            field=models.ForeignKey(to='client.CurrencyPair'),
        ),
    ]
