# Generated by Django 5.1.1 on 2024-10-05 10:20

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='auction_end_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='auction_start_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='buy_now',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='minimum_bid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='number_of_views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='promotion',
            field=models.BooleanField(default=False),
        ),
    ]
