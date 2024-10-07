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
from viewer.views import Add_auctionView, Add_auctionCreateView, Add_auctionUpdateView, Add_auctionDeleteView
from viewer.views import index, about, contact, search, podrobne_hledani, statues, jewelry, numismatics, paintings
from viewer.models import AccountStatus, AccountType, UserAccounts, Category, AddAuction, Auction
from viewer import views

from viewer.views import Add_auctionDetailView

# Registrace modelů do administrace
admin.site.register(AccountStatus)
admin.site.register(AccountType)
admin.site.register(UserAccounts)
admin.site.register(Category)
admin.site.register(AddAuction)
admin.site.register(Auction)

# Definice URL vzorů
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name='index'),
    # path("pridat_inzerat", pridat_inzerat)
    path("about/", about, name='about'),
    path("search/", search, name='search'),
    path("contact/", contact, name='contact'),
    path("podrobne_hledani/", podrobne_hledani, name="podrobne_hledani"),
    # path("inzeraty/<int:pk>/", auction, name='auction'),
    path('add_auction/', Add_auctionView.as_view(), name='add_auction'),
    path('add_auction/create', Add_auctionCreateView.as_view(), name='add_auction_add'),
    path('add_auction/update/<pk>', Add_auctionUpdateView.as_view(), name='add_auction_update'),
    path('add_auction/delete/<pk>', Add_auctionDeleteView.as_view(), name='add_auction_delete'),
    path('paintings/', paintings, name='paintings'),
    path('statues/', statues, name='statues'),
    path('jewelry/', jewelry, name='jewelry'),
    path('numismatics/', numismatics, name='numismatics'),
    path('test/', views.my_view),

    path('add_auction/<int:pk>/', views.auction_detail, name='add_auction-detail'),
]

# Přidání URL pro obsluhu mediálních souborů během vývoje
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)