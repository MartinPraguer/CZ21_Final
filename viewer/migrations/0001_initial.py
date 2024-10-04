# Generated by Django 5.1.1 on 2024-10-04 18:32

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_status', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(default='No description provided')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('minimum_bid', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('buy_now', models.BooleanField(default=False)),
                ('promotion', models.BooleanField(default=False)),
                ('auction_start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('auction_end_date', models.DateTimeField(default=datetime.datetime.now)),
                ('number_of_views', models.IntegerField(default=0)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='viewer.category')),
            ],
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='photos/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.category')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionEvalution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_rating', models.IntegerField()),
                ('sellers_comment', models.TextField()),
                ('buyer_rating', models.IntegerField()),
                ('buyers_comment', models.TextField()),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.auction')),
            ],
        ),
    ]
