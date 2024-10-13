from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from Aukce.settings import USE_TZ
from viewer.models import AddAuction, Category, Profile
from viewer.forms import AddAuctionForm, SignUpForm, BidForm
from viewer.models import AddAuction, Category, Bid
from viewer.forms import AddAuctionForm, SignUpForm
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
import logging
from django.views import View
from django.utils import timezone
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm, UserCreationForm)
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from viewer.models import Profile, UserAccounts, AccountType

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'sign_up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()

                # Zde použij vybraný typ účtu z formuláře
                account_type = form.cleaned_data.get('account_type')

                # Zkontroluj, zda již existuje záznam v UserAccounts
                if not UserAccounts.objects.filter(user=user).exists():
                    UserAccounts.objects.create(user=user, account_type=account_type)
                else:
                    form.add_error(None, 'Uživatel již má účet.')  # Pokud je potřeba, můžeš přidat vlastní chybu

                login(request, user)  # Automatické přihlášení po registraci
                return redirect('login')

            except IntegrityError:
                form.add_error(None, 'Chyba při vytváření účtu. Zkuste to prosím znovu.')

        return render(request, 'sign_up.html', {'form': form})
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




def numismatics(request):
    # Získání kategorie "Numismatics"
    numismatics_category = Category.objects.get(name="Numismatics")

    # Filtrujte pouze inzeráty s kategorií "Numismatics" a aukcemi typu "Buy Now"
    buy_now_add_auction = AddAuction.objects.filter(category=numismatics_category, auction_type='buy_now').order_by(
        "-created")[:4]

    # Aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(category=numismatics_category, promotion=True,
                                                      auction_type='place_bid').order_by("-created")[:4]

    # Aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(category=numismatics_category, promotion=False,
                                                         auction_type='place_bid').order_by("-created")[:4]

    # Přepočítáme zbývající čas u každé aukce
    for auction_list in [buy_now_add_auction, promotion_add_auction, no_promotion_add_auction]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    return render(request, template_name='numismatics.html', context={
        'buy_now_add_auctions': buy_now_add_auction,
        'promotion_add_auctions': promotion_add_auction,
        'no_promotion_add_auctions': no_promotion_add_auction
    })

def paintings(request):
    # Získání kategorie "Paintings"
    paintings_category = Category.objects.get(name="Paintings")

    # Filtrujte pouze inzeráty s kategorií "Paintings" a aukcemi typu "Buy Now"
    buy_now_add_auction = AddAuction.objects.filter(category=paintings_category, auction_type='buy_now').order_by(
        "-created")[:4]

    # Aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(category=paintings_category, promotion=True,
                                                      auction_type='place_bid').order_by("-created")[:4]

    # Aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(category=paintings_category, promotion=False,
                                                         auction_type='place_bid').order_by("-created")[:4]

    # Přepočítáme zbývající čas u každé aukce
    for auction_list in [buy_now_add_auction, promotion_add_auction, no_promotion_add_auction]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    return render(request, template_name='paintings.html', context={
        'buy_now_add_auctions': buy_now_add_auction,
        'promotion_add_auctions': promotion_add_auction,
        'no_promotion_add_auctions': no_promotion_add_auction
    })

def statues(request):
    # Získání kategorie "Statues"
    statues_category = Category.objects.get(name="Statues")

    # Filtrujte pouze inzeráty s kategorií "Statues" a aukcemi typu "Buy Now"
    buy_now_add_auction = AddAuction.objects.filter(category=statues_category, auction_type='buy_now').order_by(
        "-created")[:4]

    # Aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(category=statues_category, promotion=True,
                                                      auction_type='place_bid').order_by("-created")[:4]

    # Aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(category=statues_category, promotion=False,
                                                         auction_type='place_bid').order_by("-created")[:4]

    # Přepočítáme zbývající čas u každé aukce
    for auction_list in [buy_now_add_auction, promotion_add_auction, no_promotion_add_auction]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    return render(request, template_name='statues.html', context={
        'buy_now_add_auctions': buy_now_add_auction,
        'promotion_add_auctions': promotion_add_auction,
        'no_promotion_add_auctions': no_promotion_add_auction
    })

def jewelry(request):
    # Získání kategorie "Jewelry"
    jewelry_category = Category.objects.get(name="Jewelry")

    # Filtrujte pouze inzeráty s kategorií "Jewelry" a aukcemi typu "Buy Now"
    buy_now_add_auction = AddAuction.objects.filter(category=jewelry_category, auction_type='buy_now').order_by(
        "-created")[:4]

    # Aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(category=jewelry_category, promotion=True,
                                                      auction_type='place_bid').order_by("-created")[:4]

    # Aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(category=jewelry_category, promotion=False,
                                                         auction_type='place_bid').order_by("-created")[:4]

    # Přepočítáme zbývající čas u každé aukce
    for auction_list in [buy_now_add_auction, promotion_add_auction, no_promotion_add_auction]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    return render(request, template_name='jewelry.html', context={
        'buy_now_add_auctions': buy_now_add_auction,
        'promotion_add_auctions': promotion_add_auction,
        'no_promotion_add_auctions': no_promotion_add_auction
    })
from django.utils import timezone
from django.shortcuts import render
from .models import AddAuction, Category

def numismatics(request):
    # Získání kategorie "Numismatics"
    numismatics_category = Category.objects.get(name="Numismatics")

    # Filtrujte pouze inzeráty s kategorií "Numismatics" a aukcemi typu "Buy Now"
    buy_now_add_auction = AddAuction.objects.filter(category=numismatics_category, auction_type='buy_now').order_by(
        "-created")[:4]

    # Aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(category=numismatics_category, promotion=True,
                                                      auction_type='place_bid').order_by("-created")[:4]

    # Aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(category=numismatics_category, promotion=False,
                                                         auction_type='place_bid').order_by("-created")[:4]

    # Přepočítáme zbývající čas u každé aukce
    for auction_list in [buy_now_add_auction, promotion_add_auction, no_promotion_add_auction]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    return render(request, template_name='numismatics.html', context={
        'buy_now_add_auctions': buy_now_add_auction,
        'promotion_add_auctions': promotion_add_auction,
        'no_promotion_add_auctions': no_promotion_add_auction
    })



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
    form_class = AddAuctionForm
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
    model = AddAuction
    form_class = AddAuctionForm
    model = AddAuction
    form_class = AddAuctionForm
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
    model = AddAuction
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


from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import AddAuction, Cart

from django.shortcuts import get_object_or_404, redirect, render
from .models import AddAuction

# Funkce pro přidání do košíku
from django.shortcuts import get_object_or_404, redirect
from .models import AddAuction, Cart

def add_to_cart(request, auction_id):
    # Kontrola, zda je uživatel přihlášen
    if not request.user.is_authenticated:
        # Pokud uživatel není přihlášen, přesměruj ho na přihlašovací stránku
        return redirect('login')

    auction = get_object_or_404(AddAuction, pk=auction_id)

    if auction.buy_now_price is None:
        return redirect('auction_detail', pk=auction.pk)

    # Získáme nebo vytvoříme položku v košíku a nastavíme její cenu
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        auction=auction,
        defaults={'price': auction.buy_now_price}
    )

    if not created:
        cart_item.price = auction.buy_now_price
        cart_item.save()

    # Přesměrujeme uživatele na stránku košíku
    return redirect('cart_view')


from .models import Bid
from django.shortcuts import get_object_or_404, redirect, render
from .models import AddAuction, Bid, Cart  # Nezapomeňte importovat model košíku

from django.shortcuts import get_object_or_404, redirect, render
from .models import AddAuction, Bid, Cart  # Nezapomeňte importovat model košíku

from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import AddAuction, Bid, Cart

from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import AddAuction, Bid, Cart

from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import AddAuction, Bid, Cart


from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import AddAuction, Bid, Cart

def auction_detail(request, pk):
    auction = get_object_or_404(AddAuction, pk=pk)

    # Seřazení příhozů podle času, abychom je zobrazili chronologicky
    bids = Bid.objects.filter(auction=auction).order_by('-timestamp')

    # Kontrola, zda aukce už vypršela
    if auction.auction_end_date and auction.auction_end_date < timezone.now():
        auction_expired = True
        time_left = None  # Aukce vypršela, není zbývající čas
    else:
        auction_expired = False
        # Výpočet zbývajícího času
        time_left = auction.auction_end_date - timezone.now()

        # Přepočet sekund na dny, hodiny, minuty
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

    if request.method == 'POST':
        # Pokud aukce vypršela, zobrazíme chybovou zprávu a zamezíme příhozu
        if auction_expired:
            return render(request, 'add_auction_detail.html', {
                'auction': auction,
                'bids': bids,
                'error_message': 'Tato aukce již vypršela. Není možné přidávat příhozy.'
            })

        # Logika pro "Buy Now" typ aukce
        if auction.auction_type == 'buy_now':
            if auction.buy_now_price is None:
                return render(request, 'add_auction_detail.html', {
                    'auction': auction,
                    'bids': bids,
                    'error_message': 'Cena "Buy Now" není nastavena.'
                })
            else:
                # Přidáme do košíku
                Cart.add_to_cart(request.user, auction)
                return redirect('cart_view')

        # Logika pro "Place Bid" typ aukce
        new_bid_value = request.POST.get('new_bid')

        if new_bid_value:
            try:
                new_bid = int(new_bid_value)
            except ValueError:
                return render(request, 'add_auction_detail.html', {
                    'auction': auction,
                    'bids': bids,
                    'error_message': 'Prosím zadejte platnou částku příhozu.'
                })

            # Kontrola minimálního příhozu
            if auction.minimum_bid and new_bid < auction.minimum_bid:
                return render(request, 'add_auction_detail.html', {
                    'auction': auction,
                    'bids': bids,
                    'error_message': f'You placed a lower than minimum bid. Minimum bid is {auction.minimum_bid} Kč.'
                })

            # Pokud aukce nemá žádnou cenu, začínáme se start_price
            if auction.price is None:
                auction.price = auction.start_price

            auction.previous_price = auction.price
            auction.price += new_bid  # Zvýšíme cenu o nový příhoz

            # Uložíme nový příhoz
            Bid.objects.create(auction=auction, user=request.user, amount=new_bid)
            auction.name_bider = request.user  # Nastavení posledního přihazujícího
            auction.save()

            return redirect('add_auction-detail', pk=auction.pk)

        else:
            return render(request, 'add_auction_detail.html', {
                'auction': auction,
                'bids': bids,
                'error_message': 'Musíte zadat částku příhozu.'
            })

    return render(request, 'add_auction_detail.html', {
        'auction': auction,
        'bids': bids,
        'auction_expired': auction_expired,  # Přidáme informaci o vypršení do šablony
        'days': days if not auction_expired else 0,
        'hours': hours if not auction_expired else 0,
        'minutes': minutes if not auction_expired else 0
    })


def cart_view(request):
    # Zkontrolujeme, jestli je uživatel přihlášen
    if not request.user.is_authenticated:
        return redirect('login')

    # Získáme všechny položky v košíku pro aktuálního uživatele
    cart_items = Cart.objects.filter(user=request.user)

    # Zobrazíme stránku košíku s položkami
    return render(request, 'cart.html', {'cart_items': cart_items})

from django.shortcuts import render

def checkout_view(request):
    return render(request, 'checkout.html')



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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddAuctionForm


@login_required
def create_auction(request):
    if request.method == 'POST':
        form = AddAuctionForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)  # Vytvoří instanci, ale neuloží ji do databáze
            auction.user = request.user  # Nastaví aktuálního přihlášeného uživatele
            auction.save()  # Uloží aukci s připojeným uživatelem
            return redirect('auction_success')  # Přesměrování po úspěšném vytvoření
    else:
        form = AddAuctionForm()

    # Předání posledních aukcí do šablony
    last_auctions = AddAuction.objects.order_by("-created")[:12]
    return render(request, 'add_auction_form.html', {'form': form, 'last_auctions': last_auctions})


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import AddAuction
from .forms import AddAuctionForm
from django.views.generic.edit import CreateView
from django.contrib import messages


from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

class AddAuctionCreateView(CreateView):
    model = AddAuction
    form_class = AddAuctionForm
    template_name = 'add_auction_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Přidej do kontextu informaci, zda je uživatel přihlášen
        context['user_authenticated'] = self.request.user.is_authenticated
        return context

    def form_valid(self, form):
        # Pokud uživatel není přihlášen, přesměruje ho na login stránku
        if not self.request.user.is_authenticated:
            messages.error(self.request, "You must be logged in to create an auction.")
            return redirect(reverse('login') + f"?next={self.request.path}")

        # Pokud je uživatel přihlášen, nastavíme ho jako tvůrce aukce
        form.instance.user_creater = self.request.user
        auction = form.save()  # Uloží aukci a přiřadí ji k proměnné
        # Přesměrování na stránku úspěchu s předáním ID aukce
        return redirect(reverse('auction_success_view', kwargs={'pk': auction.pk}))



from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import AddAuction

def auction_success_view(request, pk):
    # Získej aukci na základě primárního klíče (pk)
    auction = get_object_or_404(AddAuction, pk=pk)

    # Předání aukce do kontextu
    return render(request, 'auction_success.html', {'auction': auction})


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import AddAuction

def auction_list(request):
    # Předpokládám, že máš tři typy aukcí: kup teď, promotion a bez promotion
    buy_now_add_auctions = AddAuction.objects.filter(auction_type='buy_now')
    promotion_add_auctions = AddAuction.objects.filter(auction_type='promotion')
    no_promotion_add_auctions = AddAuction.objects.filter(auction_type='no_promotion')

    # Použijeme Paginator pro každou sadu aukcí
    paginator_buy_now = Paginator(buy_now_add_auctions, 4)  # 4 položky na stránku
    paginator_promotion = Paginator(promotion_add_auctions, 4)  # 4 položky na stránku
    paginator_no_promotion = Paginator(no_promotion_add_auctions, 4)  # 4 položky na stránku

    # Získáme číslo aktuální stránky z požadavku GET (např. ?page=2)
    page_number = request.GET.get('page', 1)  # výchozí stránka 1

    # Získáme aukce pro aktuální stránku
    buy_now_page_obj = paginator_buy_now.get_page(page_number)
    promotion_page_obj = paginator_promotion.get_page(page_number)
    no_promotion_page_obj = paginator_no_promotion.get_page(page_number)

    return render(request, 'auction_list.html', {
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj,
    })









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


