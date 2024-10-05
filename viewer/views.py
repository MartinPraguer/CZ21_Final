from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render
from django.http import HttpResponse
from viewer.models import Advertisement, Category
from viewer.forms import AdvertisementForm
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
import logging



# def hello(request, s):
#     return HttpResponse(f'AHOJ {s}')

def index(request):
    return render(request, template_name='index.html', context={
        'buy_now_advertisements': Advertisement.objects.order_by("-created").filter(buy_now=True)[:4],
        'promotion_advertisements': Advertisement.objects.order_by("-created").filter(promotion=True).filter(buy_now=False)[:4],
        'no_promotion_advertisements': Advertisement.objects.order_by("-created").filter(promotion=False).filter(buy_now=False)[:4],
    })

def paintings(request):
    return render(
        request,
        "paintings.html",
        context={}
    )

def statues(request):
    return render(
        request,
        "statues.html",
        context={}
    )

def jewelry(request):
    return render(
        request,
        "jewelry.html",
        context={}
    )

def numismatics(request):
    return render(
        request,
        "numismatics.html",
        context={}
    )

def about(request):
    return render(
        request,
        "about.html",
        context={}
    )

def contact(request):
    return render(
        request,
        "contact.html",
        context={}
    )

def search(request):
    hledany_vyraz = request.GET.get('hledej', '')
    hledany_vyraz_capitalized = hledany_vyraz.capitalize()
    return render(request, template_name='search.html', context={
        "searchs": Advertisement.objects.filter(
            Q(name__icontains=hledany_vyraz) | Q(name__icontains=hledany_vyraz_capitalized) | Q(description__icontains=hledany_vyraz) | Q(description__icontains=hledany_vyraz_capitalized) | Q(user__icontains=hledany_vyraz) | Q(user__icontains=hledany_vyraz_capitalized)
        )
    })

def podrobne_hledani(request):
    name = request.GET.get('name', '')
    user = request.GET.get('user', '')
    category_name = request.GET.get('category', '')

    advertisements = Advertisement.objects.filter()

    if name:
        advertisements = advertisements.filter(name__icontains=name)
    if user:
        advertisements = advertisements.filter(user__username__icontains=user)
    if category_name and category_name != '--Category--':  # Zkontrolujte, že hodnota není výchozí
        advertisements = advertisements.filter(category__name__icontains=category_name)


    categorys = Category.objects.all()


    return render(request, template_name='podrobne_hledani.html', context={
        "advertisements": advertisements,
        "categorys": categorys,

    })


    template_name = 'form.html'
class AdvertisementView(TemplateView):
    template_name = 'advertisement.html'
    extra_context = {'advertisements': Advertisement.objects.order_by("-created")[:12]}
class AdvertisementCreateView(CreateView):
    template_name = 'advertisement_form.html'
    form_class = AdvertisementForm
    success_url = reverse_lazy('advertisement')
class AdvertisementUpdateView(UpdateView):
    template_name = 'advertisement_form.html'
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy('advertisement')
class AdvertisementDeleteView(DeleteView):
    template_name = 'advertisement_form.html'
    model = Advertisement
    success_url = reverse_lazy('building')



logger = logging.getLogger(__name__)

def my_view(request):
    # Zalogujte HTTP_HOST
    logger.info(f"Received HTTP_HOST: {request.META.get('HTTP_HOST')}")
    return HttpResponse("Hello, World!")


























# STÁHNUTO OD MARTINA Z SDACIA
# def pridat_inzerat(request):
#     # Pokud je požadavek typu POST, zpracujeme data z formuláře
#     if request.method == 'POST':
#         popis = request.POST.get('popis')
#         znacka_id = request.POST.get('znacka')
#         karoserie_id = request.POST.get('karoserie')
#         vykon = request.POST.get('vykon')
#         rok_vyroby = request.POST.get('rok_vyroby')
#         cena = request.POST.get('cena')
#
#         # Vytvoření nového inzerátu a uložení do databáze
#         inzerat = Inzeraty(
#             popis=popis,
#             znacka_id=znacka_id,
#             karoserie_id=karoserie_id,
#             vykon=vykon,
#             rok_vyroby=rok_vyroby,
#             cena=cena,
#             datum_pridani=datetime.now()
#         )
#         inzerat.save()
#
#         # Přesměrování zpět na hlavní stránku nebo kdekoliv je to potřeba
#         return redirect('index')
#
#     # Pokud je požadavek typu GET, zobrazíme formulář
#     znacky = ZnackyAut.objects.all()
#     karoserie = TypKaroserie.objects.all()
#
#     return render(request, template_name='pridat_inzerat.html', context={
#         'znacky': znacky,
#         'karoserie': karoserie
#     })


