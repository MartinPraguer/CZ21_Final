from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render
from django.http import HttpResponse
from viewer.models import Advertisement
from viewer.forms import AdvertisementForm
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q

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
            Q(name__icontains=hledany_vyraz) | Q(name__icontains=hledany_vyraz_capitalized) | Q(description__icontains=hledany_vyraz) | Q(description__icontains=hledany_vyraz_capitalized) | Q(user__icontains=hledany_vyraz) | Q(user__icontains=hledany_vyraz_capitalized)
        )
    })

def podrobne_hledani(request):
    popis = request.GET.get('popis', '')
    znacka = request.GET.get('znacka', '')
    karoserie = request.GET.get('karoserie', '')
    vykon = request.GET.get('vykon', '')
    rok_vyroby_od = request.GET.get('rok_vyroby_od', '')
    rok_vyroby_do = request.GET.get('rok_vyroby_do', '')
    cena_od = request.GET.get('cena_od', '')
    cena_do = request.GET.get('cena_do', '')
    datum_pridani_od = request.GET.get('datum_pridani_od', '')
    datum_pridani_do = request.GET.get('datum_pridani_do', '')

    inzeraty = Advertisement.objects.filter()

    # if popis:
    #     inzeraty = inzeraty.filter(popis__icontains=popis)
    # if znacka:
    #     inzeraty = inzeraty.filter(znacka__znacka__icontains=znacka)
    # if karoserie:
    #     inzeraty = inzeraty.filter(karoserie__karoserie__icontains=karoserie)
    # if vykon:
    #     inzeraty = inzeraty.filter(vykon__icontains=vykon)
    # if rok_vyroby_od:
    #     inzeraty = inzeraty.filter(rok_vyroby__gte=rok_vyroby_od)  # Rok výroby od
    # if rok_vyroby_do:
    #     inzeraty = inzeraty.filter(rok_vyroby__lte=rok_vyroby_do)  # Rok výroby do
    # if cena_od:
    #     inzeraty = inzeraty.filter(cena__gte=cena_od)
    # if cena_do:
    #     inzeraty = inzeraty.filter(cena__lte=cena_do)
    # if datum_pridani_od:
    #     inzeraty = inzeraty.filter(datum_pridani__date__gte=datum_pridani_od)  # Datum přidání od
    # if datum_pridani_do:
    #     inzeraty = inzeraty.filter(datum_pridani__date__lte=datum_pridani_do)  # Datum přidání do
    #
    # znacky = ZnackyAut.objects.all()
    # karoserie = TypKaroserie.objects.all()

    return render(request, template_name='podrobne_hledani.html', context={
        # "inzeraty": inzeraty,
        # "znacky": znacky,
        # "karoserie": karoserie
    })


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


