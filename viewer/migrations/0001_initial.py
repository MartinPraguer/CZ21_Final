import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

def create_account_types(apps, schema_editor):
    AccountType = apps.get_model('viewer', 'AccountType')
    AccountType.objects.get_or_create(account_type='User')
    AccountType.objects.get_or_create(account_type='Premium')
    AccountType.objects.get_or_create(account_type='Superuser')

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
            name='AddAuction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos/')),
                ('name_auction', models.CharField(max_length=128)),
                ('description', models.TextField(default='No description provided')),
                ('promotion', models.BooleanField(default=False)),
                ('auction_start_date', models.DateTimeField(auto_now_add=True)),
                ('auction_end_date', models.DateTimeField(auto_now_add=True)),
                ('number_of_views', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('auction_type', models.CharField(choices=[('buy_now', 'Buy Now'), ('place_bid', 'Place Bid')], default='place_bid', max_length=10)),
                ('buy_now_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('start_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('previous_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('minimum_bid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('name_bider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bided_auctions', to=settings.AUTH_USER_MODEL)),
                ('name_buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='listed_auctions', to=settings.AUTH_USER_MODEL)),
                ('user_creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_auctions', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.category')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='viewer.addauction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.addauction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('auction_start_date', models.DateTimeField(auto_now_add=True)),
                ('auction_end_date', models.DateTimeField(auto_now_add=True)),
                ('number_of_views', models.IntegerField(default=0)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='viewer.category')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='City', max_length=128)),
                ('address', models.CharField(default='Address', max_length=256)),
                ('zip_code', models.CharField(default='00000', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('account_status', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.accountstatus')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_rating', models.IntegerField()),
                ('sellers_comment', models.TextField()),
                ('buyer_rating', models.IntegerField()),
                ('buyers_comment', models.TextField()),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.auction')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.accounttype')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_account_types),  # Přidání této řádky
    ]