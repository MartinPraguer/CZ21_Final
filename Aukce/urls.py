"""
URL configuration for Aukce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from viewer.views import AddauctionUpdateView, AddauctionDeleteView, authors, add_evaluation
from viewer.views import index, detailed_search,   AddAuctionCreateView, auction_success_view, add_to_cart, cart_view, checkout_view,  user_detail, list_users, success_page, success_delete
from viewer.models import AccountStatus, AccountType, UserAccounts, Category, AddAuction, Cart
from viewer.views import index, about_us,  AddAuctionCreateView, auction_success_view, add_to_cart, cart_view, checkout_view
from viewer.models import AccountStatus, AccountType, UserAccounts, Category, AddAuction, Cart, Profile
from viewer.views_sablony import statues, jewelry, numismatics, paintings, paintings, last_auction, current_auctions, auction_archives, statues, jewelry, numismatics
from viewer import views
from viewer.views import PaymentView
from django.contrib.auth.views import LogoutView
from viewer.views import SignUpView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView



# Registrace modelů do administrace
admin.site.register(AccountStatus)
admin.site.register(AccountType)
admin.site.register(UserAccounts)
admin.site.register(Category)
admin.site.register(AddAuction)
# admin.site.register(Auction)
admin.site.register(Cart)
admin.site.register(Profile)
from django.contrib.auth.models import Permission
admin.site.register(Permission)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('auctions/', views.auctions, name='auctions'),



    path("", index, name='index'),
    path('paintings/', paintings, name='paintings'),
    path('statues/', statues, name='statues'),
    path('jewelry/', jewelry, name='jewelry'),
    path('numismatics/', numismatics, name='numismatics'),
    path('current_auctions/', current_auctions, name='current_auctions'),
    path('auction_archives/', auction_archives, name='auction_archives'),
    path("detailed_search/", detailed_search, name="detailed_search"),
    path('last_auction/', last_auction, name='last_auction'),
    path('about_us/', about_us, name='about_us'),



    path('add_auction/<int:pk>/', views.auction_detail, name='add_auction_detail'),
    path('add_auction/create/', AddAuctionCreateView.as_view(), name='add_auction_create'),
    path('auction_success/<int:pk>/', views.auction_success_view, name='auction_success_view'),
    path('add_auction/update/<pk>', AddauctionUpdateView.as_view(), name='add_auction_update'),
    path('add_auction/delete/<pk>', AddauctionDeleteView.as_view(), name='add_auction_delete'),
    path('success_delete/<str:auction_title>/', success_delete, name='success_delete'),
    path('add_auction/confirm_delete/<int:pk>/', AddauctionDeleteView.as_view(), name='confirm_delete'),



    path('list_users/', list_users, name='list_users'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('auction/<int:auction_id>/add_evaluation/<str:user_type>/', views.add_evaluation, name='add_evaluation'),



    path('add_to_cart/<int:auction_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment/<str:payment_type>/', PaymentView.as_view(), name='payment'),
    path('success/', TemplateView.as_view(template_name="success.html"), name='success'),
    path('error/', TemplateView.as_view(template_name="error.html"), name='error'),
    path('checkout/', views.PaymentView.as_view(), name='checkout'),
    path('pay/', views.pay_button, name='pay_button'),
    path('success/', views.success_page, name='success_page'),
]

# Přidání URL pro obsluhu mediálních souborů během vývoje
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)