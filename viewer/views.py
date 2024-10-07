from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render
from django.http import HttpResponse
from viewer.models import Add_auction, Category
from viewer.forms import Add_auctionForm
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
import logging



# def hello(request, s):
#     return HttpResponse(f'AHOJ {s}')

def index(request):
    return render(request, template_name='base_4_obrazky.html', context={
        'buy_now_add_auction': Add_auction.objects.order_by("-created").filter(buy_now=True)[:4],
        'promotion_add_auction': Add_auction.objects.order_by("-created").filter(promotion=True).filter(buy_now=False)[:4],
        'no_promotion_add_auction': Add_auction.objects.order_by("-created").filter(promotion=False).filter(buy_now=False)[:4],
    })


def paintings(request):
    # Získání kategorie "Paintings"
    paintings_category = Category.objects.get(name="Paintings")

    # Filtrujte pouze inzeráty s kategorií "Paintings"
    buy_now_add_auction = Add_auction.objects.filter(category=paintings_category, buy_now=True).order_by(
        "-created")[:4]
    promotion_add_auction = Add_auction.objects.filter(category=paintings_category, promotion=True,
                                                            buy_now=False).order_by("-created")[:4]
    no_promotion_add_auction = Add_auction.objects.filter(category=paintings_category, promotion=False,
                                                               buy_now=False).order_by("-created")[:4]

    return render(request, template_name='paintings.html', context={
        'buy_now_add_auctions': buy_now_add_auction,
        'promotion_add_auctions': promotion_add_auction,
        'no_promotion_add_auctions': no_promotion_add_auction,
    })


def statues(request):
    # Získání kategorie "Statues"
    statues_category = Category.objects.get(name="Statues")

    # Filtrujte pouze inzeráty s kategorií "Statues"
    buy_now_add_auction = Add_auction.objects.filter(category=statues_category, buy_now=True).order_by(
        "-created")[:4]
    promotion_add_auction = Add_auction.objects.filter(category=statues_category, promotion=True,
                                                            buy_now=False).order_by("-created")[:4]
    no_promotion_add_auction = Add_auction.objects.filter(category=statues_category, promotion=False,
                                                               buy_now=False).order_by("-created")[:4]

    return render(request, template_name='statues.html', context={
        'buy_now_add_auctions': buy_now_add_auction,
        'promotion_add_auctions': promotion_add_auction,
        'no_promotion_add_auctions': no_promotion_add_auction,
    })


def jewelry(request):
    # Získání kategorie "Jewelry"
    jewelry_category = Category.objects.get(name="Jewelry")

    # Filtrujte pouze inzeráty s kategorií "Jewelry"
    buy_now_add_auction = Add_auction.objects.filter(category=jewelry_category, buy_now=True).order_by(
        "-created")[:4]
    promotion_add_auction = Add_auction.objects.filter(category=jewelry_category, promotion=True,
                                                            buy_now=False).order_by("-created")[:4]
    no_promotion_add_auction = Add_auction.objects.filter(category=jewelry_category, promotion=False,
                                                               buy_now=False).order_by("-created")[:4]

    return render(request, template_name='jewelry.html', context={
        'buy_now_add_auctions': buy_now_add_auction,
        'promotion_add_auctions': promotion_add_auction,
        'no_promotion_add_auctions': no_promotion_add_auction,
    })


def numismatics(request):
    # Získání kategorie "Numismatics"
    numismatics_category = Category.objects.get(name="Numismatics")

    # Filtrujte pouze inzeráty s kategorií "Nummismatics"
    buy_now_add_auction = Add_auction.objects.filter(category=numismatics_category, buy_now=True).order_by(
        "-created")[:4]
    promotion_add_auction = Add_auction.objects.filter(category=numismatics_category, promotion=True,
                                                            buy_now=False).order_by("-created")[:4]
    no_promotion_add_auction = Add_auction.objects.filter(category=numismatics_category, promotion=False,
                                                               buy_now=False).order_by("-created")[:4]

    return render(request, template_name='numismatics.html', context={
        'buy_now_add_auctions': buy_now_add_auction,
        'promotion_add_auctions': promotion_add_auction,
        'no_promotion_add_auctions': no_promotion_add_auction,
    })

# def numismatics(request):
#     return render(
#         request,
#         "numismatics.html",
#         context={}
#     )

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
        "searchs": Add_auction.objects.filter(
            Q(name__icontains=hledany_vyraz) | Q(name__icontains=hledany_vyraz_capitalized) | Q(description__icontains=hledany_vyraz) | Q(description__icontains=hledany_vyraz_capitalized) | Q(user__icontains=hledany_vyraz) | Q(user__icontains=hledany_vyraz_capitalized)
        )
    })

def podrobne_hledani(request):
    name = request.GET.get('name', '')
    user = request.GET.get('user', '')
    category_name = request.GET.get('category', '')

    add_auction = Add_auction.objects.filter()

    if name:
        add_auction = add_auction.filter(name__icontains=name)
    if user:
        add_auction = add_auction.filter(user__username__icontains=user)
    if category_name and category_name != '--Category--':  # Zkontrolujte, že hodnota není výchozí
        add_auction = add_auction.filter(category__name__icontains=category_name)


    categorys = Category.objects.all()


    return render(request, template_name='podrobne_hledani.html', context={
        "add_auction": add_auction,
        "categorys": categorys,

    })


    template_name = 'form.html'
class Add_auctionView(TemplateView):
    template_name = 'add_auction.html'
    extra_context = {'add_auction': Add_auction.objects.order_by("-created")[:12]}
class Add_auctionCreateView(CreateView):
    template_name = 'add_auction_form.html'
    form_class = Add_auctionForm
    success_url = reverse_lazy('add_auction')
class Add_auctionUpdateView(UpdateView):
    template_name = 'add_auction_form.html'
    model = Add_auction
    form_class = Add_auctionForm
    success_url = reverse_lazy('add_auction')
class Add_auctionDeleteView(DeleteView):
    template_name = 'add_auction_form.html'
    model = Add_auction
    success_url = reverse_lazy('add_auction')



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


