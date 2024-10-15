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
from viewer.views import AddauctionUpdateView, AddauctionDeleteView, AddauctionView, current_auctions, auction_archives, authors
from viewer.views import index, about, detailed_search, statues, jewelry, numismatics, paintings, AddAuctionCreateView, auction_success_view, add_to_cart, cart_view, checkout_view,  user_detail, list_users, success_page, last_auction
from viewer.models import AccountStatus, AccountType, UserAccounts, Category, AddAuction, Cart
from viewer.views import index, about, statues, jewelry, numismatics, paintings, AddAuctionCreateView, auction_success_view, add_to_cart, cart_view, checkout_view
from viewer.models import AccountStatus, AccountType, UserAccounts, Category, AddAuction, Cart, Profile
from viewer import views
from viewer.views import PaymentView
from viewer.views import AddauctionDetailView
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

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name='index'),
    # path("pridat_inzerat", pridat_inzerat)
    path("about/", about, name='about'),
    # path("search/", search, name='search'),
    path("detailed_search/", detailed_search, name="detailed_search"),
    # path("inzeraty/<int:pk>/", auction, name='auction'),
    # path('add_auction/create', add_auction, name='add_auction'),
    path('add_auction/', AddauctionView.as_view(), name='add_auction'),
    path('add_auction/create/', AddAuctionCreateView.as_view(), name='add_auction_create'),
    path('auction_success/<int:pk>/', views.auction_success_view, name='auction_success_view'),  # Přidána URL pro úspěšné vytvoření aukce
    path('add_auction/update/<pk>', AddauctionUpdateView.as_view(), name='add_auction_update'),
    path('add_auction/delete/<pk>', AddauctionDeleteView.as_view(), name='add_auction_delete'),
    path('paintings/', paintings, name='paintings'),
    path('statues/', statues, name='statues'),
    path('jewelry/', jewelry, name='jewelry'),
    path('numismatics/', numismatics, name='numismatics'),
    path('last_auction/', last_auction, name='last_auction'),
    # path('test/', views.my_view),
    # path('add_auction/<int:pk>/', AddauctionDetailView.as_view(), name='add_auction-detail'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add_auction/<int:pk>/', views.auction_detail, name='add_auction-detail'),
    path('current_auctions/', current_auctions, name='current_auctions'),
    path('auction_archives/', auction_archives, name='auction_archives'),
    path('authors/', authors, name='authors'),
    path('add_to_cart/<int:auction_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment/<str:payment_type>/', PaymentView.as_view(), name='payment'),
    path('success/', TemplateView.as_view(template_name="success.html"), name='success'),
    path('error/', TemplateView.as_view(template_name="error.html"), name='error'),
    path('list_users/', list_users, name='list_users'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('cart/', views.cart_view, name='cart_view'),  # URL pro zobrazení košíku
    path('checkout/', views.PaymentView.as_view(), name='checkout'),  # URL pro platbu
    path('pay/', views.pay_button, name='pay_button'),
    path('success/', views.success_page, name='success_page'),
]

# Přidání URL pro obsluhu mediálních souborů během vývoje
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)