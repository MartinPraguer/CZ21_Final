from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from Aukce.settings import USE_TZ
from viewer.models import AddAuction, Category, Profile
from viewer.forms import AddAuctionForm, SignUpForm, BidForm
from viewer.models import AddAuction, Category, Bid, Cart
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
from viewer.models import Profile, UserAccounts, AccountType, Cart

from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.http import JsonResponse




class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'sign_up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()

                # Vybraný typ účtu z formuláře
                account_type = form.cleaned_data.get('account_type')

                # Zkontroluj, zda již existuje záznam v UserAccounts
                if not UserAccounts.objects.filter(user=user).exists():
                    user_account = UserAccounts.objects.create(user=user, account_type=account_type)

                    # Pokud uživatel vybere prémiový účet, nastav předplatné
                    if account_type.account_type == 'Premium':
                        user_account.set_premium_subscription()

                    login(request, user)  # Automatické přihlášení po registraci
                    return redirect('login')
                else:
                    form.add_error(None, 'Uživatel již má účet.')

            except IntegrityError:
                form.add_error(None, 'Chyba při vytváření účtu. Zkuste to prosím znovu.')

        return render(request, 'sign_up.html', {'form': form})

# platebni brana a odkazy na vyzkouseni Pro předplatné: http://localhost:8000/payment/subscription/
# Pro košík: http://localhost:8000/payment/cart/

class PaymentView(View):
    def get(self, request, payment_type):
        user = request.user
        cart_total_amount = 0

        if payment_type == 'cart':
            # Získej celkovou cenu z košíku
            cart_total_amount = Cart.objects.filter(user=user).aggregate(total=models.Sum('price'))['total'] or 0

        context = {
            'payment_type': payment_type,
            'stripe_public_key': 'YOUR_STRIPE_PUBLIC_KEY',  # Nahraď svým veřejným klíčem
            'cart_total_amount': cart_total_amount,  # Přidáno pro košík
        }
        return render(request, 'payment.html', context)

    def post(self, request, payment_type):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        user = request.user

        if payment_type == 'subscription':
            # Cena za předplatné
            amount = 25000  # 250 Kč v haléřích
            description = 'Předplatné'
        elif payment_type == 'cart':
            # Získej celkovou cenu z košíku
            cart_total = Cart.objects.filter(user=user).aggregate(total=models.Sum('price'))['total'] or 0
            amount = int(cart_total * 100)  # Celková cena v haléřích
            description = 'Celková cena za košík'
        else:
            return JsonResponse({'error': 'Neplatný typ platby'}, status=400)

        # Vytvoření checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'czk',
                        'product_data': {
                            'name': description,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )

        return JsonResponse({'id': session.id})

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

    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte pouze inzeráty s kategorií "Jewelry" a aukcemi typu "Buy Now", které ještě neskončily
    buy_now_add_auction = AddAuction.objects.filter(
        category=paintings_category,
        auction_type='buy_now',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(
        category=paintings_category,
        promotion=True,
        auction_type='place_bid',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(
        category=paintings_category,
        promotion=False,
        auction_type='place_bid',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Vytvoření paginatoru pro jednotlivé aukce
    paginator_buy_now = Paginator(buy_now_add_auction, 8)  # 8 aukcí na stránku
    paginator_promotion = Paginator(promotion_add_auction, 8)
    paginator_no_promotion = Paginator(no_promotion_add_auction, 8)

    # Získání čísla stránky
    page_number = request.GET.get('page')

    # Získání aukcí pro konkrétní stránku
    buy_now_page_obj = paginator_buy_now.get_page(page_number)
    promotion_page_obj = paginator_promotion.get_page(page_number)
    no_promotion_page_obj = paginator_no_promotion.get_page(page_number)

    # Přepočítáme zbývající čas u každé aukce po stránkování
    for auction_list in [buy_now_page_obj, promotion_page_obj, no_promotion_page_obj]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    return render(request, template_name='paintings.html', context={
        'page_name': 'Jewelry',
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })

from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render

def statues(request):
    # Získání kategorie "statues"
    statues_category = Category.objects.get(name="Statues")

    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte pouze inzeráty s kategorií "Jewelry" a aukcemi typu "Buy Now", které ještě neskončily
    buy_now_add_auction = AddAuction.objects.filter(
        category=statues_category,
        auction_type='buy_now',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(
        category=statues_category,
        promotion=True,
        auction_type='place_bid',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(
        category=statues_category,
        promotion=False,
        auction_type='place_bid',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Vytvoření paginatoru pro jednotlivé aukce
    paginator_buy_now = Paginator(buy_now_add_auction, 8)  # 8 aukcí na stránku
    paginator_promotion = Paginator(promotion_add_auction, 8)
    paginator_no_promotion = Paginator(no_promotion_add_auction, 8)

    # Získání čísla stránky
    page_number = request.GET.get('page')

    # Získání aukcí pro konkrétní stránku
    buy_now_page_obj = paginator_buy_now.get_page(page_number)
    promotion_page_obj = paginator_promotion.get_page(page_number)
    no_promotion_page_obj = paginator_no_promotion.get_page(page_number)

    # Přepočítáme zbývající čas u každé aukce po stránkování
    for auction_list in [buy_now_page_obj, promotion_page_obj, no_promotion_page_obj]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    return render(request, template_name='statues.html', context={
        'page_name': 'Jewelry',
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })


from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from .models import AddAuction, Category

def jewelry(request):
    # Získání kategorie "Jewelry"
    jewelry_category = Category.objects.get(name="Jewelry")

    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte pouze inzeráty s kategorií "Jewelry" a aukcemi typu "Buy Now", které ještě neskončily
    buy_now_add_auction = AddAuction.objects.filter(
        category=jewelry_category,
        auction_type='buy_now',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(
        category=jewelry_category,
        promotion=True,
        auction_type='place_bid',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(
        category=jewelry_category,
        promotion=False,
        auction_type='place_bid',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Vytvoření paginatoru pro jednotlivé aukce
    paginator_buy_now = Paginator(buy_now_add_auction, 8)  # 8 aukcí na stránku
    paginator_promotion = Paginator(promotion_add_auction, 8)
    paginator_no_promotion = Paginator(no_promotion_add_auction, 8)

    # Získání čísla stránky
    page_number = request.GET.get('page')

    # Získání aukcí pro konkrétní stránku
    buy_now_page_obj = paginator_buy_now.get_page(page_number)
    promotion_page_obj = paginator_promotion.get_page(page_number)
    no_promotion_page_obj = paginator_no_promotion.get_page(page_number)

    # Přepočítáme zbývající čas u každé aukce po stránkování
    for auction_list in [buy_now_page_obj, promotion_page_obj, no_promotion_page_obj]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    return render(request, template_name='jewelry.html', context={
        'page_name': 'Jewelry',
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })


from django.utils import timezone
from django.shortcuts import render
from .models import AddAuction, Category

def numismatics(request):
    # Získání kategorie "Numismatics"
    numismatics_category = Category.objects.get(name="Numismatics")

    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte pouze inzeráty s kategorií "Jewelry" a aukcemi typu "Buy Now", které ještě neskončily
    buy_now_add_auction = AddAuction.objects.filter(
        category=numismatics_category,
        auction_type='buy_now',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(
        category=numismatics_category,
        promotion=True,
        auction_type='place_bid',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(
        category=numismatics_category,
        promotion=False,
        auction_type='place_bid',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Vytvoření paginatoru pro jednotlivé aukce
    paginator_buy_now = Paginator(buy_now_add_auction, 8)  # 8 aukcí na stránku
    paginator_promotion = Paginator(promotion_add_auction, 8)
    paginator_no_promotion = Paginator(no_promotion_add_auction, 8)

    # Získání čísla stránky
    page_number = request.GET.get('page')

    # Získání aukcí pro konkrétní stránku
    buy_now_page_obj = paginator_buy_now.get_page(page_number)
    promotion_page_obj = paginator_promotion.get_page(page_number)
    no_promotion_page_obj = paginator_no_promotion.get_page(page_number)

    # Přepočítáme zbývající čas u každé aukce po stránkování
    for auction_list in [buy_now_page_obj, promotion_page_obj, no_promotion_page_obj]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    return render(request, template_name='numismatics.html', context={
        'page_name': 'Jewelry',
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
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

from django.db.models import Q

# def search(request):
#     hledany_vyraz = request.GET.get('Search', '').strip()
#     hledany_vyraz_capitalized = hledany_vyraz.capitalize()
#
#     return render(request, template_name='detailed_search.html', context={
#         "searchs": AddAuction.objects.filter(
#             Q(name_auction__icontains=hledany_vyraz) |
#             Q(name_auction__icontains=hledany_vyraz_capitalized) |
#             Q(description__icontains=hledany_vyraz) |
#             Q(description__icontains=hledany_vyraz_capitalized) |
#             Q(user_creator__username__icontains=hledany_vyraz) |  # Filtr na username
#             Q(user_creator__username__icontains=hledany_vyraz_capitalized) |
#             Q(user_creator__first_name__icontains=hledany_vyraz) |  # Filtr na jméno
#             Q(user_creator__first_name__icontains=hledany_vyraz_capitalized) |
#             Q(user_creator__last_name__icontains=hledany_vyraz) |  # Filtr na příjmení
#             Q(user_creator__last_name__icontains=hledany_vyraz_capitalized)
#         )
#     })
from django.shortcuts import render
from .forms import AuctionSearchForm
from .models import AddAuction
from django.db.models import Q
def detailed_search(request):
    hledany_vyraz = request.GET.get('Search', '').strip()
    hledany_vyraz_capitalized = hledany_vyraz.capitalize()

    form = AuctionSearchForm(request.GET or None)
    auctions = AddAuction.objects.all()

    if form.is_valid():
        # Filtrace podle názvu aukce (pomocí formuláře)
        name_auction = form.cleaned_data.get('name_auction')
        if name_auction:
            auctions = auctions.filter(Q(name_auction__icontains=name_auction))

        # Filtrace podle kategorie
        category = form.cleaned_data.get('category')
        if category:
            auctions = auctions.filter(category=category)

        # Filtrace podle typu aukce
        auction_type = form.cleaned_data.get('auction_type')
        if auction_type:
            auctions = auctions.filter(auction_type=auction_type)

        # Filtrace podle ceny
        price_from = form.cleaned_data.get('price_from')
        price_to = form.cleaned_data.get('price_to')
        if price_from:
            auctions = auctions.filter(price__gte=price_from)
        if price_to:
            auctions = auctions.filter(price__lte=price_to)

        # Filtrace podle ceny Buy Now
        buy_now_price_from = form.cleaned_data.get('buy_now_price_from')
        buy_now_price_to = form.cleaned_data.get('buy_now_price_to')
        if buy_now_price_from:
            auctions = auctions.filter(buy_now_price__gte=buy_now_price_from)
        if buy_now_price_to:
            auctions = auctions.filter(buy_now_price__lte=buy_now_price_to)

        # Filtrace podle data začátku aukce
        auction_start_date_from = form.cleaned_data.get('auction_start_date_from')
        auction_start_date_to = form.cleaned_data.get('auction_start_date_to')
        if auction_start_date_from:
            auctions = auctions.filter(auction_start_date__gte=auction_start_date_from)
        if auction_start_date_to:
            auctions = auctions.filter(auction_start_date__lte=auction_start_date_to)

        # Filtrace podle data konce aukce
        auction_end_date_from = form.cleaned_data.get('auction_end_date_from')
        auction_end_date_to = form.cleaned_data.get('auction_end_date_to')
        if auction_end_date_from:
            auctions = auctions.filter(auction_end_date__gte=auction_end_date_from)
        if auction_end_date_to:
            auctions = auctions.filter(auction_end_date__lte=auction_end_date_to)

    # Filtrace podle hledaného výrazu (search)
    if hledany_vyraz:
        auctions = auctions.filter(
            Q(name_auction__icontains=hledany_vyraz) |
            Q(name_auction__icontains=hledany_vyraz_capitalized) |
            Q(description__icontains=hledany_vyraz) |
            Q(description__icontains=hledany_vyraz_capitalized) |
            Q(user_creator__username__icontains=hledany_vyraz) |
            Q(user_creator__username__icontains=hledany_vyraz_capitalized) |
            Q(user_creator__first_name__icontains=hledany_vyraz) |  # Opravený zápis
            Q(user_creator__first_name__icontains=hledany_vyraz_capitalized) |  # Opravený zápis
            Q(user_creator__last_name__icontains=hledany_vyraz) |
            Q(user_creator__last_name__icontains=hledany_vyraz_capitalized)
        )

    return render(request, 'detailed_search.html', {'form': form, 'searchs': auctions})




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

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import AddAuction, Bid

def auction_detail(request, pk):
    auction = get_object_or_404(AddAuction, pk=pk)

    # Seřazení příhozů podle času, abychom je zobrazili chronologicky
    bids = Bid.objects.filter(auction=auction).order_by('-timestamp')

    # Kontrola, zda aukce už vypršela
    auction_expired = auction.auction_end_date and auction.auction_end_date < timezone.now()

    if auction_expired:
        time_left = None  # Aukce vypršela, není zbývající čas
    else:
        # Výpočet zbývajícího času
        time_left = auction.auction_end_date - timezone.now()

        # Přepočet sekund na dny, hodiny, minuty
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

    if request.method == 'POST':
        # Pokud aukce vypršela, zobrazíme chybovou zprávu a zamezíme příhozu nebo koupi
        if auction_expired:
            return render(request, 'add_auction_detail.html', {
                'auction': auction,
                'bids': bids,
                'error_message': 'Tato aukce již vypršela. Není možné přidávat příhozy ani koupit položku.'
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
                # Přidáme do košíku pouze pokud aukce nevypršela
                if not auction_expired:
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

    # Předejte proměnné do šablony
    return render(request, 'add_auction_detail.html', {
        'auction': auction,
        'bids': bids,
        'auction_expired': auction_expired,  # Informace o vypršení aukce
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



from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render

def auction_archives(request):
    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte pouze inzeráty s aukcemi typu "Buy Now", které již skončily
    buy_now_add_auction = AddAuction.objects.filter(auction_type='buy_now', auction_end_date__lt=current_time).order_by("-created")

    # Aukce s propagací, které nejsou "Buy Now", které již skončily
    promotion_add_auction = AddAuction.objects.filter(promotion=True, auction_type='place_bid', auction_end_date__lt=current_time).order_by("-created")

    # Aukce bez propagace, které nejsou "Buy Now", které již skončily
    no_promotion_add_auction = AddAuction.objects.filter(promotion=False, auction_type='place_bid', auction_end_date__lt=current_time).order_by("-created")

    # Vytvoření paginatoru pro jednotlivé aukce
    paginator_buy_now = Paginator(buy_now_add_auction, 8)  # 8 aukcí na stránku
    paginator_promotion = Paginator(promotion_add_auction, 8)
    paginator_no_promotion = Paginator(no_promotion_add_auction, 8)

    # Získání čísla stránky
    page_number = request.GET.get('page')

    # Získání aukcí pro konkrétní stránku
    buy_now_page_obj = paginator_buy_now.get_page(page_number)
    promotion_page_obj = paginator_promotion.get_page(page_number)
    no_promotion_page_obj = paginator_no_promotion.get_page(page_number)

    # Přepočítáme zbývající čas u každé aukce po stránkování
    for auction_list in [buy_now_page_obj, promotion_page_obj, no_promotion_page_obj]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    # Předejte název stránky
    return render(request, template_name='auction_archives.html', context={
        'page_name': 'Auction Archives',  # Předání názvu stránky
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })

def current_auctions(request):
    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte pouze inzeráty s aukcemi typu "Buy Now", které ještě neskončily
    buy_now_add_auction = AddAuction.objects.filter(
        auction_type='buy_now',
        auction_end_date__gt=current_time  # Aukce, které ještě neskončily
    ).order_by("auction_end_date")  # Seřadit podle nejbližšího konce

    # Aukce s propagací, které nejsou "Buy Now", a ještě neskončily
    promotion_add_auction = AddAuction.objects.filter(
        promotion=True,
        auction_type='place_bid',
        auction_end_date__gt=current_time  # Aukce, které ještě neskončily
    ).order_by("auction_end_date")  # Seřadit podle nejbližšího konce

    # Aukce bez propagace, které nejsou "Buy Now", a ještě neskončily
    no_promotion_add_auction = AddAuction.objects.filter(
        promotion=False,
        auction_type='place_bid',
        auction_end_date__gt=current_time  # Aukce, které ještě neskončily
    ).order_by("auction_end_date")  # Seřadit podle nejbližšího konce

    # Vytvoření paginatoru pro jednotlivé aukce
    paginator_buy_now = Paginator(buy_now_add_auction, 8)  # 8 aukcí na stránku
    paginator_promotion = Paginator(promotion_add_auction, 8)
    paginator_no_promotion = Paginator(no_promotion_add_auction, 8)

    # Získání čísla stránky
    page_number = request.GET.get('page')

    # Získání aukcí pro konkrétní stránku
    buy_now_page_obj = paginator_buy_now.get_page(page_number)
    promotion_page_obj = paginator_promotion.get_page(page_number)
    no_promotion_page_obj = paginator_no_promotion.get_page(page_number)

    # Přepočítáme zbývající čas u každé aukce po stránkování
    for auction_list in [buy_now_page_obj, promotion_page_obj, no_promotion_page_obj]:
        for auction in auction_list:
            if auction.auction_end_date and auction.auction_end_date > timezone.now():
                time_left = auction.auction_end_date - timezone.now()
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    # Předejte název stránky
    return render(request, template_name='current_auctions.html', context={
        'page_name': 'Current Auctions',  # Předání názvu stránky
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
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
        form.instance.user_creator = self.request.user
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

def auction_list1(request):
    # Získání všech aukcí pro kategorii numismatika
    buy_now_auctions = AddAuction.objects.filter(auction_type='buy_now')
    promotion_auctions = AddAuction.objects.filter(promotion=True)
    no_promotion_auctions = AddAuction.objects.filter(promotion=False)

    # Stránkování pro každou sadu aukcí
    paginator_buy_now = Paginator(buy_now_auctions, 8)  # 5 aukcí na stránku
    paginator_promotion = Paginator(promotion_auctions, 8)
    paginator_no_promotion = Paginator(no_promotion_auctions, 8)

    # Získáme číslo aktuální stránky
    page_number_buy_now = request.GET.get('buy_now_page', 1)
    page_number_promotion = request.GET.get('promotion_page', 1)
    page_number_no_promotion = request.GET.get('no_promotion_page', 1)

    # Získáme aukce pro aktuální stránku
    buy_now_page_obj = paginator_buy_now.get_page(page_number_buy_now)
    promotion_page_obj = paginator_promotion.get_page(page_number_promotion)
    no_promotion_page_obj = paginator_no_promotion.get_page(page_number_no_promotion)

    context = {
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj,
    }
    return render(request, 'auction_list1.html', context)



def auction_list2(request):
    # Získání všech aukcí pro kategorii numismatika
    buy_now_auctions = AddAuction.objects.filter(auction_type='buy_now')
    promotion_auctions = AddAuction.objects.filter(promotion=True)
    no_promotion_auctions = AddAuction.objects.filter(promotion=False)

    # Stránkování pro každou sadu aukcí
    paginator_buy_now = Paginator(buy_now_auctions, 8)  # 5 aukcí na stránku
    paginator_promotion = Paginator(promotion_auctions, 8)
    paginator_no_promotion = Paginator(no_promotion_auctions, 8)

    # Získáme číslo aktuální stránky
    page_number_buy_now = request.GET.get('buy_now_page', 1)
    page_number_promotion = request.GET.get('promotion_page', 1)
    page_number_no_promotion = request.GET.get('no_promotion_page', 1)

    # Získáme aukce pro aktuální stránku
    buy_now_page_obj = paginator_buy_now.get_page(page_number_buy_now)
    promotion_page_obj = paginator_promotion.get_page(page_number_promotion)
    no_promotion_page_obj = paginator_no_promotion.get_page(page_number_no_promotion)

    context = {
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj,
    }
    return render(request, 'auction_list2.html', context)


from django.core.paginator import Paginator


def auction_list3(request):
    # Předpokládám, že máš aukce uložené ve 'buy_now_add_auctions', 'promotion_add_auctions' a 'no_promotion_add_auctions'

    auctions = AddAuction.objects.all()  # Tvůj dotaz pro získání všech aukcí

    # Získáme číslo stránky z parametru GET
    page_number = request.GET.get('page', 1)  # Default na první stránku

    # Nastav paginátor (např. 10 aukcí na stránku)
    paginator = Paginator(auctions, 10)

    # Získáme aukce pro aktuální stránku
    page_obj = paginator.get_page(page_number)

    return render(request, 'auction_list3.html', {
        'page_obj': page_obj,  # Pošli objekt s paginací do šablony
    })

from django.contrib.auth.models import User
from django.shortcuts import render

def list_users(request):
    user_creator = User.objects.all()  # Získání všech uživatelů
    return render(request, 'list_users.html', {'users': user_creator})


from django.contrib.auth.models import User
from .models import AddAuction
from django.shortcuts import render, get_object_or_404


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Získání uživatele na základě jeho ID
    created_auctions = user.created_auctions.all()  # Aukce, které uživatel vytvořil
    bided_auctions = user.bided_auctions.all()  # Aukce, kde uživatel přihazoval
    bought_auctions = user.listed_auctions.all()  # Aukce, které uživatel koupil

    return render(request, 'user_detail.html', {
        'user': user,
        'created_auctions': created_auctions,
        'bided_auctions': bided_auctions,
        'bought_auctions': bought_auctions,
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


