from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from viewer.models import UserAccounts, AccountType

@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    # Vytvoření nebo získání typů účtů
    account_user, created = AccountType.objects.get_or_create(account_type='User')
    account_premium, created = AccountType.objects.get_or_create(account_type='Premium')

    # Vytvoření Superusera
    superuser_username = 'superuser'
    if not User.objects.filter(username=superuser_username).exists():
        superuser = User.objects.create_superuser(
            username=superuser_username,
            password='superpassword',
            email='superuser@example.com'
        )
        UserAccounts.objects.create(user=superuser, account_type=account_premium)

    # Vytvoření Premium uživatele
    premium_username = 'premiumuser'
    if not User.objects.filter(username=premium_username).exists():
        premium_user = User.objects.create_user(
            username=premium_username,
            password='premiumpassword',
            email='premium@example.com'
        )
        premium_user.is_staff = True  # Premium uživatelé mají přístup do administrace
        premium_user.save()
        UserAccounts.objects.create(user=premium_user, account_type=account_premium)

    # Vytvoření běžného uživatele
    normal_username = 'ordinaryuser'
    if not User.objects.filter(username=normal_username).exists():
        normal_user = User.objects.create_user(
            username=normal_username,
            password='userpassword',
            email='ordinary@example.com'
        )
        UserAccounts.objects.create(user=normal_user, account_type=account_user)
