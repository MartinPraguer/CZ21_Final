# Generated by Django 5.1.1 on 2024-10-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0005_alter_advertisement_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='buy_now',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='promotion',
            field=models.BooleanField(default=False),
        ),
    ]
