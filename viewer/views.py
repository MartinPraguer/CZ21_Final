from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render
from django.http import HttpResponse
from viewer.models import Advertisement
from viewer.forms import AdvertisementForm
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy

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


# def pridat_inzerat(request):
#
#
#     return render(
#          request,
#          "pridat_inzerat.html",
#          context={}
#     )


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


