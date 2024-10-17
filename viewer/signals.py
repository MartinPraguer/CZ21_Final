# from django.contrib.auth.models import User
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from viewer.models import UserAccounts, AccountType
#
# @receiver(post_migrate)
# def create_default_users(sender, **kwargs):
#     # Vytvoření nebo získání typů účtů
#     account_user, created = AccountType.objects.get_or_create(account_type='User')
#     account_premium, created = AccountType.objects.get_or_create(account_type='Premium')
#
#     # Vytvoření Superusera
#     if not User.objects.filter(username='superuser').exists():
#         superuser = User.objects.create_superuser(
#             username='superuser',
#             password='superpassword',
#             email='superuser@example.com'
#         )
#         superuser.save()
#
#     # Vytvoření Premium uživatele
#     if not User.objects.filter(username='premiumuser').exists():
#         premium_user = User.objects.create_user(
#             username='premiumuser',
#             password='premiumpassword',
#             email='premium@example.com'
#         )
#         premium_user.is_staff = True  # Premium uživatelé mají přístup do administrace
#         premium_user.save()
#
#         # Přiřazení Premium role
#         UserAccounts.objects.create(user=premium_user, account_type=account_premium)
#
#     # Vytvoření běžného uživatele
#     if not User.objects.filter(username='ordinaryuser').exists():
#         normal_user = User.objects.create_user(
#             username='ordinaryuser',
#             password='userpassword',
#             email='ordinary@example.com'
#         )
#         UserAccounts.objects.create(user=normal_user, account_type=account_user)
#         normal_user.save()
