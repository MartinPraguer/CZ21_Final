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
from django.urls import path, include
from viewer.views import Add_auctionView, Add_auctionCreateView, Add_auctionUpdateView, Add_auctionDeleteView
from django.urls import path
from viewer.views import Add_auctionCreateView, Add_auctionUpdateView, Add_auctionDeleteView, Add_auctionView, current_auctions, auction_archives, authors, shopping_cart
from viewer.views import index, about, contact, search, podrobne_hledani, statues, jewelry, numismatics, paintings, AddAuctionCreateView, auction_success_view, add_to_cart, cart_view, checkout_view, auction_list1, auction_list2, auction_list3
from viewer.models import AccountStatus, AccountType, UserAccounts, Category, AddAuction, Auction, Cart
from viewer import views

from viewer.views import Add_auctionDetailView
from django.contrib.auth.views import LogoutView
from viewer.views import SignUpView
from django.contrib.auth import views as auth_views



# Registrace modelů do administrace
admin.site.register(AccountStatus)
admin.site.register(AccountType)
admin.site.register(UserAccounts)
admin.site.register(Category)
admin.site.register(AddAuction)
admin.site.register(Auction)
admin.site.register(Cart)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name='index'),
    # path("pridat_inzerat", pridat_inzerat)
    path("about/", about, name='about'),
    path("search/", search, name='search'),
    path("contact/", contact, name='contact'),
    path("podrobne_hledani/", podrobne_hledani, name="podrobne_hledani"),
    # path("inzeraty/<int:pk>/", auction, name='auction'),
    # path('add_auction/create', add_auction, name='add_auction'),
    path('add_auction/', Add_auctionView.as_view(), name='add_auction'),
    path('add_auction/create/', AddAuctionCreateView.as_view(), name='add_auction_create'),
    path('auction_success/<int:pk>/', views.auction_success_view, name='auction_success_view'),  # Přidána URL pro úspěšné vytvoření aukce
    path('add_auction/update/<pk>', Add_auctionUpdateView.as_view(), name='add_auction_update'),
    path('add_auction/delete/<pk>', Add_auctionDeleteView.as_view(), name='add_auction_delete'),
    path('paintings/', paintings, name='paintings'),
    path('statues/', statues, name='statues'),
    path('jewelry/', jewelry, name='jewelry'),
    path('numismatics/', numismatics, name='numismatics'),
    path('test/', views.my_view),
    # path('add_auction/<int:pk>/', Add_auctionDetailView.as_view(), name='add_auction-detail'),
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

    path('auction_list1/', auction_list1, name='auction_list1'),
    path('auction_list2/', auction_list2, name='auction_list2'),
    path('auction_list3/', auction_list3, name='auction_list3'),
]

# Přidání URL pro obsluhu mediálních souborů během vývoje
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)