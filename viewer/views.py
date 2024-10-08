from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render
from django.http import HttpResponse

from Aukce.settings import USE_TZ
from viewer.models import Add_auction, Category, Profile
from viewer.forms import AddAuctionForm, SignUpForm
from viewer.models import AddAuction, Category
from viewer.forms import Add_auctionForm
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
import logging
from django.utils import timezone
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm, UserCreationForm)


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')  # Po úspěšné registraci přesměruje na stránku přihlášení
    template_name = 'sign_up.html'

# def hello(request, s):
#     return HttpResponse(f'AHOJ {s}')

def add_auction(request):
    last_auctions = AddAuction.objects.all() #.order_by("-created")[:16]
    print(last_auctions)  # Debug: zjistit, jestli jsou nějaké aukce
    return render(request, template_name='base_4_obrazky.html', context={
        "last_auctions": last_auctions,})


        # 'buy_now_add_auction': AddAuction.objects.order_by("-created").filter(buy_now=True)[:4],
        # 'promotion_add_auction': AddAuction.objects.order_by("-created").filter(promotion=True).filter(buy_now=False)[:4],
        # 'no_promotion_add_auction': AddAuction.objects.order_by("-created").filter(promotion=False).filter(buy_now=False)[:4],



def index(request):
    return render(request, template_name='base_4_obrazky.html', context={
    # return render(request, template_name='add_auction.html', context={
    #     "last_auctions": AddAuction.objects.order_by("-created")[:16],
        # 'buy_now_add_auction': AddAuction.objects.order_by("-created").filter(buy_now=True)[:4],
        # 'promotion_add_auction': AddAuction.objects.order_by("-created").filter(promotion=True).filter(buy_now=False)[:4],
        # 'no_promotion_add_auction': AddAuction.objects.order_by("-created").filter(promotion=False).filter(buy_now=False)[:4],
    })


def paintings(request):
    # Získání kategorie "Paintings"
    paintings_category = Category.objects.get(name="Paintings")

    # Filtrujte pouze inzeráty s kategorií "Paintings"
    buy_now_add_auction = AddAuction.objects.filter(category=paintings_category, buy_now=True).order_by(
        "-created")[:4]
    promotion_add_auction = AddAuction.objects.filter(category=paintings_category, promotion=True,
                                                      buy_now=False).order_by("-created")[:4]
    no_promotion_add_auction = AddAuction.objects.filter(category=paintings_category, promotion=False,
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
    buy_now_add_auction = AddAuction.objects.filter(category=statues_category, buy_now=True).order_by(
        "-created")[:4]
    promotion_add_auction = AddAuction.objects.filter(category=statues_category, promotion=True,
                                                      buy_now=False).order_by("-created")[:4]
    no_promotion_add_auction = AddAuction.objects.filter(category=statues_category, promotion=False,
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
    buy_now_add_auction = AddAuction.objects.filter(category=jewelry_category, buy_now=True).order_by(
        "-created")[:4]
    promotion_add_auction = AddAuction.objects.filter(category=jewelry_category, promotion=True,
                                                      buy_now=False).order_by("-created")[:4]
    no_promotion_add_auction = AddAuction.objects.filter(category=jewelry_category, promotion=False,
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
    buy_now_add_auction = AddAuction.objects.filter(category=numismatics_category, buy_now=True).order_by(
        "-created")[:4]
    promotion_add_auction = AddAuction.objects.filter(category=numismatics_category, promotion=True,
                                                      buy_now=False).order_by("-created")[:4]
    no_promotion_add_auction = AddAuction.objects.filter(category=numismatics_category, promotion=False,
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
        "searchs": AddAuction.objects.filter(
            Q(name__icontains=hledany_vyraz) | Q(name__icontains=hledany_vyraz_capitalized) | Q(description__icontains=hledany_vyraz) | Q(description__icontains=hledany_vyraz_capitalized) | Q(user__icontains=hledany_vyraz) | Q(user__icontains=hledany_vyraz_capitalized)
        )
    })

def podrobne_hledani(request):
    name = request.GET.get('name', '')
    user = request.GET.get('user', '')
    category_name = request.GET.get('category', '')

    add_auction = AddAuction.objects.filter()

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
    extra_context = {'last_auctions': AddAuction.objects.order_by("-created")[:12]}
class Add_auctionCreateView(CreateView):
    model = AddAuction
    form_class = Add_auctionForm
    template_name = 'add_auction_add.html'  # Název vaší šablony
    success_url = reverse_lazy('add_auction_create')  # Přesměrování po úspěšném vytvoření záznamu

    def get_context_data(self, **kwargs):
        # Přidání dalších dat do kontextu
        context = super().get_context_data(**kwargs)
        context['last_auctions'] = AddAuction.objects.order_by("-created")[:12]
        return context
    template_name = 'add_auction_form.html'
    form_class = AddAuctionForm
    success_url = reverse_lazy('add_auction')
class Add_auctionUpdateView(UpdateView):
    template_name = 'add_auction_form.html'
    model = Add_auction
    form_class = AddAuctionForm
    model = AddAuction
    form_class = Add_auctionForm
    success_url = reverse_lazy('add_auction')
class Add_auctionDeleteView(DeleteView):
    template_name = 'add_auction_form.html'
    model = AddAuction
    success_url = reverse_lazy('add_auction')



logger = logging.getLogger(__name__)

def my_view(request):
    # Zalogujte HTTP_HOST
    logger.info(f"Received HTTP_HOST: {request.META.get('HTTP_HOST')}")
    return HttpResponse("Hello, World!")


from django.views.generic.detail import DetailView

# zobrazení detailu konkretniho inzeratu

class Add_auctionDetailView(DetailView):
    model = Add_auction
    template_name = 'add_auction_detail.html'
    context_object_name = 'add_auction'
class Add_auctionDetailView(DetailView):
    model = AddAuction
    template_name = 'add_auction_detail.html'
    context_object_name = 'add_auction'

    # metoda na zvyšování počtu zobrazení po každém kliknutí

    def get_object(self, queryset=None):
        add_auction = super().get_object(queryset)
        add_auction.number_of_views += 1
        add_auction.save()
        return add_auction



from django.shortcuts import render, get_object_or_404, redirect
from .models import AddAuction, Bid
from .forms import BidForm


def auction_detail(request, pk):
    add_auction = get_object_or_404(AddAuction, pk=pk)
    bids = add_auction.bids.all().order_by('-timestamp')

    # Získání posledního příhozu (nejvyšší nabídky), pokud existuje
    last_bid = bids.first() if bids.exists() else None

    # Uložení `last_price` (cena před posledním příhozem)
    last_price = add_auction.price

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.add_auction = add_auction
            bid.user = request.user  # Předpoklad, že uživatel je přihlášen

            # Uložení `last_price` před aktualizací ceny
            add_auction.last_price = add_auction.price

            # Aktualizace ceny aukce na základě nové nabídky
            add_auction.price += bid.amount  # Nová cena po přičtení příhozu
            add_auction.save()
            bid.save()

            return redirect('add_auction-detail', pk=add_auction.pk)
    else:
        form = BidForm()

    return render(request, 'add_auction_detail.html', {
        'add_auction': add_auction,
        'bids': bids,
        'form': form,
        'last_price': last_price,  # Přidání `last_price` do kontextu
    })

def current_auctions(request):
    return HttpResponse(f'AHOJ')

def auction_archives(request):

    auction_archives = AddAuction.objects.filter(auction_end_date__lt=timezone.now()).order_by('-created')[:16]


    return render(request, template_name='auction_archives.html', context={
        'auction_archives': auction_archives,
    })


def authors(request):
    return HttpResponse(f'AHOJ')

def shopping_cart(request):
    return HttpResponse(f'AHOJ')





















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


