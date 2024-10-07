from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render, redirect
from django.http import HttpResponse
from viewer.models import Advertisement
from viewer.forms import AdvertisementForm
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Auction



# def hello(request, s):
#     return HttpResponse(f'AHOJ {s}')
#
# # Create your views here.
def index(request):
    return render(
        request,
        "index.html",
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
            Q(name__icontains=hledany_vyraz) | Q(name__icontains=hledany_vyraz_capitalized) | Q(description__icontains=hledany_vyraz) | Q(description__icontains=hledany_vyraz_capitalized)
        )
    })

def auction(request, pk):
    aukce = Auction.objects.get(pk=pk)

    aukce.pocet_zobrazeni += 1
    aukce.save()

    if request.method == 'POST':
        # Získat data z formuláře
        nick = request.POST.get('nick')
        text = request.POST.get('text')

        # Vytvořit a uložit nový komentář
        # komentar = Komentare(
        #     nick=nick,
        #     text=text,
        #     auction=aukce
        # )
        # komentar.save()

        # Přesměrování na stejnou stránku, aby se zobrazil nový komentář
        return redirect('auction', pk=aukce.pk)

    return render(request, template_name='auction.html', context={'aukce': aukce})

def ongoing_auctions(request):
    # Filter auctions that are currently running
    auctions = Auction.objects.filter(
        auction_start_date__lte=timezone.now(),
        auction_end_date__gte=timezone.now()
    )
    return render(request, 'ongoing_auctions.html', {'auctions': auctions})


    template_name = 'form.html'
class AdvertisementView(TemplateView):
    template_name = 'advertisement.html'
    extra_context = {'advertisements': Advertisement.objects.all()}
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


