# Generated by Django 5.1.1 on 2024-10-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0017_rename_last_price_addauction_previous_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addauction',
            name='start_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
