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
from viewer.views import AdvertisementView, AdvertisementCreateView, AdvertisementUpdateView, AdvertisementDeleteView
from viewer.views import index, about, contact, search, podrobne_hledani, statues, jewelry, numismatics, paintings
from viewer.models import AccountStatus, AccountType, UserAccounts, Category, Advertisement, Auction

# Registrace modelů do administrace
admin.site.register(AccountStatus)
admin.site.register(AccountType)
admin.site.register(UserAccounts)
admin.site.register(Category)
admin.site.register(Advertisement)
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
    path('advertisement/', AdvertisementView.as_view(), name='advertisement'),
    path('advertisement/create', AdvertisementCreateView.as_view(), name='advertisement_add'),
    path('advertisement/update/<pk>', AdvertisementUpdateView.as_view(), name='advertisement_update'),
    path('advertisement/delete/<pk>', AdvertisementDeleteView.as_view(), name='advertisement_delete'),
    path('paintings/', paintings, name='paintings'),
    path('statues/', statues, name='statues'),
    path('jewelry/', jewelry, name='jewelry'),
    path('numismatics/', numismatics, name='numismatics'),
]

# Přidání URL pro obsluhu mediálních souborů během vývoje
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)