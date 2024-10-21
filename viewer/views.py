from django.http import HttpResponse
from viewer.forms import SignUpForm
from django.views.generic import UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
import logging
from django.contrib.auth import login
from viewer.models import UserAccounts
from django.db import IntegrityError
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import stripe
from .models import Category
from .forms import AuctionSearchForm
from django.db.models import Q
from django.views.generic.detail import DetailView
from .models import Cart, About
from django.utils import timezone
from .models import Bid
from django.contrib.auth.decorators import login_required
from .forms import AddAuctionForm
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import AddAuction
from .models import AddAuction, AuctionImage
from django.db import transaction
from viewer.models import Profile
from django.http import HttpResponseForbidden
from django.db import transaction  # Přidej tento import
from django.shortcuts import redirect
from .models import Cart, ArchivedPurchase, UserAccounts
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import AddAuction, TransactionEvaluation, User
from django.db.models import Avg
from .forms import SellerEvaluationForm, BuyerEvaluationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import AddAuction, TransactionEvaluation
from .forms import SellerEvaluationForm, BuyerEvaluationForm

























from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import AddAuction, TransactionEvaluation, UserAccounts
from .forms import SellerEvaluationForm, BuyerEvaluationForm
from django.db.models import Avg


@login_required
def add_evaluation(request, auction_id):
    auction = get_object_or_404(AddAuction, id=auction_id)
    print(f"Auction found: {auction.name_auction}")

    # Kontrola, zda už uživatel (prodávající nebo kupující) již udělil hodnocení
    if request.user == auction.user_creator:
        evaluation_exists = TransactionEvaluation.objects.filter(auction=auction, seller=request.user).exists()
    else:
        evaluation_exists = TransactionEvaluation.objects.filter(auction=auction, buyer=request.user).exists()

    if evaluation_exists:
        print("Uživatel již udělil hodnocení.")
        return redirect('add_auction_detail', pk=auction.id)

    # Rozdělení formuláře pro prodávajícího nebo kupujícího
    if request.user == auction.user_creator:
        print("User is the seller")
        if request.method == 'POST':
            seller_form = SellerEvaluationForm(request.POST)
            if seller_form.is_valid():
                evaluation = seller_form.save(commit=False)
                evaluation.auction = auction
                evaluation.seller = request.user  # Nastavení prodávajícího
                evaluation.buyer = auction.name_buyer  # Přiřadíme kupujícího z aukce
                print(f"Hodnocení připraveno k uložení: Seller Rating - {evaluation.seller_rating}")
                evaluation.save()
                print("Seller evaluation saved successfully")
                return redirect('add_auction_detail', pk=auction.id)
            else:
                print("Seller form is not valid")
                print(seller_form.errors)
        else:
            seller_form = SellerEvaluationForm()
        return render(request, 'add_evaluation.html', {
            'form': seller_form,
            'is_seller': True,
            'auction': auction,
        })

    elif auction.name_buyer and request.user == auction.name_buyer:
        print("User is the buyer")
        if request.method == 'POST':
            buyer_form = BuyerEvaluationForm(request.POST)
            if buyer_form.is_valid():
                evaluation = buyer_form.save(commit=False)
                evaluation.auction = auction
                evaluation.buyer = request.user  # Nastavení kupujícího
                evaluation.seller = auction.user_creator  # Přiřazení prodávajícího
                print(f"Hodnocení připraveno k uložení: Buyer Rating - {evaluation.buyer_rating}")
                evaluation.save()
                print("Buyer evaluation saved successfully")
                return redirect('add_auction_detail', pk=auction.id)
            else:
                print("Buyer form is not valid")
                print(buyer_form.errors)
        else:
            buyer_form = BuyerEvaluationForm()

        return render(request, 'add_evaluation.html', {
            'form': buyer_form,
            'is_seller': False,
            'auction': auction,
        })
    else:
        print("Uživatel není oprávněn hodnotit tuto aukci.")
        return redirect('add_auction_detail', pk=auction.id)


@login_required
def user_detail(request, user_id):
    # Kontrola, zda je uživatel Premium nebo Superuser
    user_account = UserAccounts.objects.get(user=request.user)
    if user_account.account_type.account_type == 'Premium' or request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)  # Získání detailů uživatele

        # Aukce vytvořené uživatelem
        created_auctions = user.created_auctions.all()
        # Aukce, kde uživatel přihazoval
        bided_auctions = user.bided_auctions.all()
        # Aukce, které uživatel koupil
        bought_auctions = user.listed_auctions.all()

        # Získání průměrného hodnocení jako kupujícího
        average_buyer_rating = user.buyer_reviews.aggregate(Avg('buyer_rating'))['buyer_rating__avg']

        # Získání průměrného hodnocení jako prodávajícího
        average_seller_rating = user.seller_reviews.aggregate(Avg('seller_rating'))['seller_rating__avg']

        # Získání hodnocení, která uživatel udělil jako kupující
        given_buyer_reviews = TransactionEvaluation.objects.filter(buyer=user)

        # Získání hodnocení, která uživatel udělil jako prodávající
        given_seller_reviews = TransactionEvaluation.objects.filter(seller=user)

        return render(request, 'user_detail.html', {
            'user': user,
            'created_auctions': created_auctions,
            'bided_auctions': bided_auctions,
            'bought_auctions': bought_auctions,
            'average_buyer_rating': average_buyer_rating,
            'average_seller_rating': average_seller_rating,
            'given_buyer_reviews': given_buyer_reviews,  # Přidání udělených hodnocení jako kupující
            'given_seller_reviews': given_seller_reviews,  # Přidání udělených hodnocení jako prodávající
        })
    else:
        return HttpResponseForbidden("Nemáte oprávnění pro zobrazení detailů uživatele.")





# add_evaluation.html
@login_required
def auctions(request):
    # Získáme všechny aukce vytvořené přihlášeným uživatelem
    auctions = AddAuction.objects.filter(user_creator=request.user)

    # Předáme aukce do šablony
    return render(request, 'auctions.html', {'auctions': auctions})


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    user = request.user
    return render(request, 'profile.html', {'user': user, 'profile': profile})


@login_required
def edit_profile(request):
    # Získáme aktuální uživatelský profil a informace o uživateli
    profile = request.user.profile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Přesměrování na stránku profilu po uložení

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def success_page(request):
    return render(request, 'success.html')


@login_required
def pay_button(request):
    if request.method == 'POST':
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            # Pokud je košík prázdný, přesměruj uživatele zpět
            return redirect('cart')

        # Přesuneme položky z košíku do archivovaných nákupů
        for item in cart_items:
            # Vytvoříme záznam v Archivovaných položkách
            ArchivedPurchase.objects.create(
                user=user,
                auction=item.auction,
                price=item.price
            )

            # Označíme aukci jako zakoupenou
            auction = item.auction
            auction.name_buyer = user  # Uložíme uživatele jako kupujícího
            auction.auction_end_date = timezone.now()  # Ukončíme aukci
            auction.is_sold = True  # Nastavíme aukci jako prodanou
            auction.save()

        # Vymažeme položky z košíku
        cart_items.delete()

        # Zvýšíme počet nákupů uživatele
        user_account = UserAccounts.objects.get(user=user)
        user_account.purchase_count += 1
        user_account.save()

        return redirect('success')  # Přesměruj na stránku potvrzení

    return redirect('cart')


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, './registration/sign_up.html', {'form': form})

    @transaction.atomic  # Přidej atomic blok, aby všechny operace byly buď úspěšné, nebo se vrátí zpět
    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)

                # Uložení uživatele před vytvořením dalších objektů
                user.save()  # Uložíme uživatele do databáze, aby s ním šlo pracovat

                # Vybraný typ účtu z formuláře
                account_type = form.cleaned_data.get('account_type')

                # Zkontroluj, zda již existuje záznam v UserAccounts
                if not UserAccounts.objects.filter(user=user).exists():
                    # Vytvoříme UserAccounts po uložení uživatele
                    user_account = UserAccounts.objects.create(user=user, account_type=account_type)

                    # Pokud uživatel vybere prémiový účet, nastav předplatné
                    if account_type.account_type == 'Premium':
                        user_account.set_premium_subscription()

                    # Vytvoříme také profil uživatele
                    Profile.objects.create(
                        user=user,
                        city=form.cleaned_data['city'],
                        address=form.cleaned_data['address'],
                        zip_code=form.cleaned_data['zip_code'],
                        avatar=form.cleaned_data.get('avatar')  # Volitelné, pokud je avatar vyplněn
                    )

                    login(request, user)  # Automatické přihlášení po registraci
                    return redirect('index')
                else:
                    form.add_error(None, 'Uživatel již má účet.')

            except IntegrityError:
                form.add_error(None, 'Chyba při vytváření účtu. Zkuste to prosím znovu.')

        return render(request, './registration/sign_up.html', {'form': form})


# platebni brana a odkazy na vyzkouseni Pro předplatné: http://localhost:8000/payment/subscription/
# Pro košík: http://localhost:8000/payment/cart/


class PaymentView(View):
    def get(self, request, payment_type):
        user = request.user
        cart_total_amount = 0

        if payment_type == 'cart':
            # Získej celkovou cenu z košíku
            cart_total_amount = Cart.get_cart_total(user)
            cart_total_amount_in_halere = int(cart_total_amount * 100)  # Převod na haléře

        context = {
            'payment_type': payment_type,
            'stripe_public_key': 'YOUR_STRIPE_PUBLIC_KEY',  # Nahraď svým veřejným klíčem
            'cart_total_amount': cart_total_amount,  # Celková cena pro zobrazení
            'cart_total_amount_in_halere': cart_total_amount_in_halere if payment_type == 'cart' else 25000,
            # Cena v haléřích
            'cart_items': Cart.objects.filter(user=user),  # Zobrazení položek v košíku
        }
        return render(request, 'payment.html', context)

    def post(self, request, payment_type):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user = request.user

        if payment_type == 'subscription':
            # Cena za předplatné
            amount = 25000  # 250 Kč v haléřích
            description = 'Předplatné'
            line_items = [{
                'price_data': {
                    'currency': 'czk',
                    'product_data': {
                        'name': description,
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }]
        elif payment_type == 'cart':
            # Získej celkovou cenu z košíku
            cart_total = Cart.get_cart_total(user)
            amount = int(cart_total * 100)  # Celková cena v haléřích
            description = 'Celková cena za košík'

            # Vytvoříme řádky pro každou položku v košíku
            cart_items = Cart.objects.filter(user=user)
            line_items = []
            for item in cart_items:
                line_items.append({
                    'price_data': {
                        'currency': 'czk',
                        'product_data': {
                            'name': item.auction.name_auction,  # Název aukce/položky
                        },
                        'unit_amount': int(item.price * 100),  # Cena v haléřích
                    },
                    'quantity': 1,
                })

            if not line_items:
                return JsonResponse({'error': 'Košík je prázdný'}, status=400)
        else:
            return JsonResponse({'error': 'Neplatný typ platby'}, status=400)

        # Vytvoření checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,  # Odeslání všech položek v košíku
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )

        return JsonResponse({'id': session.id})

    template_name = 'form.html'


class AddAuctionCreateView(CreateView):
    model = AddAuction
    form_class = AddAuctionForm
    template_name = 'add_auction_form.html'

    def get_context_data(self, **kwargs):
        # Získání původního kontextu z nadřazené třídy
        context = super().get_context_data(**kwargs)
        context['last_auctions'] = AddAuction.objects.order_by("-created")[:12]  # Přidání posledních aukcí
        context['user_authenticated'] = self.request.user.is_authenticated  # Informace o přihlášení uživatele
        return context

    def form_valid(self, form):
        # Pokud není uživatel přihlášen, přesměrujeme ho na login stránku
        if not self.request.user.is_authenticated:
            messages.error(self.request, "Musíte být přihlášeni, abyste mohli přidat aukci.")
            return redirect(reverse('login') + f"?next={self.request.path}")

        # Nastavení tvůrce aukce na aktuálního přihlášeného uživatele
        form.instance.user_creator = self.request.user
        auction = form.save(commit=False)  # Uložení aukce bez odeslání do databáze

        # Nastavení promotion na základě typu účtu
        auction.promotion = self.request.user.useraccounts.account_type.account_type == 'Premium'

        auction.save()  # Uložení aukce do databáze

        # Zpracování nahraných obrázků
        images = form.cleaned_data['images']
        for image in images:
            AuctionImage.objects.create(auction=auction, image=image)

        # Přesměrování na stránku úspěchu po vytvoření aukce
        return redirect(reverse('auction_success_view', kwargs={'pk': auction.pk}))


class AddauctionUpdateView(UpdateView):
    model = AddAuction
    form_class = AddAuctionForm
    template_name = 'add_auction_form.html'

    def get_success_url(self):
        # Po úspěšné aktualizaci se uživatel přesměruje na stránku úspěchu
        return reverse('auction_success_view', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auction'] = self.object  # Přidání aukce do kontextu
        return context


class AddauctionDeleteView(DeleteView):
    model = AddAuction
    template_name = 'confirm_delete.html'  # Šablona pro potvrzení smazání

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auction'] = self.get_object()  # Získání aukce a její předání do šablony
        return context

    def get_success_url(self):
        auction_title = self.object.name_auction  # Získání názvu aukce
        return reverse('success_delete', kwargs={'auction_title': auction_title})

    def delete(self, request, *args, **kwargs):
        auction = self.get_object()  # Získání aukce, která má být smazána
        auction.delete()  # Aukce je smazána
        return redirect(self.get_success_url())  # Přesměrování po úspěšném smazání


def success_delete(request, auction_title):
    # Zobrazí stránku s potvrzením úspěšného smazání
    return render(request, 'success_delete.html', {'auction_title': auction_title})


# class AddauctionDetailView(DetailView):
#     model = AddAuction
#     template_name = 'add_auction_detail.html'
#     context_object_name = 'add_auction'
#
#     # metoda na zvyšování počtu zobrazení po každém kliknutí
#
#     def get_object(self, queryset=None):
#         add_auction = super().get_object(queryset)
#         add_auction.number_of_views += 1
#         add_auction.save()
#         return add_auction


def add_to_cart(request, auction_id):
    # Kontrola, zda je uživatel přihlášen

    # Kontrola, zda je uživatel přihlášen
    if not request.user.is_authenticated:
        # Přesměrování na login s parametrem next
        return redirect(f'{reverse("login")}?next={request.path}')

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


# Funkce pro zobrazení a správu košíku
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Zpracování přidání položky do košíku ze stránky aukcí
    auction_id = request.GET.get('add_auction_id')
    if auction_id:
        auction = get_object_or_404(AddAuction, id=auction_id)
        Cart.add_to_cart(request.user, auction)
        return redirect('cart_view')

    # Zpracování odstranění položky z košíku
    remove_auction_id = request.GET.get('remove_auction_id')
    if remove_auction_id:
        cart_item = Cart.objects.filter(user=request.user, auction_id=remove_auction_id).first()
        if cart_item:
            cart_item.delete()

    # Získání položek v košíku
    cart_items = Cart.objects.filter(user=request.user)
    cart_total_amount = Cart.get_cart_total(request.user)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
    })


def checkout_view(request):
    return render(request, 'checkout.html')


@permission_required("viewer.add_category")
def authors(request):
    return HttpResponse(f'AHOJ')


@login_required
def create_auction(request):
    if request.method == 'POST':
        form = AddAuctionForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user_creator = request.user  # Nastavení uživatele, který aukci vytvořil

            # Kontrola, zda je uživatel Premium
            user_account = UserAccounts.objects.get(user=request.user)
            if user_account.account_type.account_type == 'Premium':
                auction.promotion = True  # Automatická propagace pro Premium uživatele
            else:
                auction.promotion = False  # Běžní uživatelé nemají propagaci

            auction.save()  # Uložení aukce
            return redirect('auction_success')
    else:
        form = AddAuctionForm()

    return render(request, 'add_auction_form.html', {'form': form})


def auction_success_view(request, pk):
    # Získej aukci na základě primárního klíče (pk)
    auction = get_object_or_404(AddAuction, pk=pk)

    # Předání aukce do kontextu
    return render(request, 'auction_success.html', {'auction': auction})


@login_required
def list_users(request):
    # Zjistíme, zda je uživatel Premium nebo Superuser
    user_account = UserAccounts.objects.get(user=request.user)
    if user_account.account_type.account_type == 'Premium' or request.user.is_superuser:
        users = User.objects.all()  # Získání všech uživatelů
        return render(request, 'list_users.html', {'users': users})
    else:
        return HttpResponseForbidden("Nemáte oprávnění pro zobrazení ostatních uživatelů.")


def user_review(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Získání průměrného hodnocení
    average_rating = user.reviews_received.aggregate(Avg('buyer_rating'))['buyer_rating__avg']

    return render(request, 'user_review.html', {
        'user': user,
        'average_rating': average_rating
    })


@login_required
def user_detail(request, user_id):
    # Kontrola, zda je uživatel Premium nebo Superuser
    user_account = UserAccounts.objects.get(user=request.user)
    if user_account.account_type.account_type == 'Premium' or request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)  # Získání detailů uživatele
        created_auctions = user.created_auctions.all()  # Aukce vytvořené uživatelem
        bided_auctions = user.bided_auctions.all()  # Aukce, kde uživatel přihazoval
        bought_auctions = user.listed_auctions.all()  # Aukce, které uživatel koupil

        # Získání průměrného hodnocení jako kupujícího
        average_buyer_rating = user.buyer_reviews.aggregate(Avg('buyer_rating'))['buyer_rating__avg']

        # Pokud chceš i hodnocení jako prodávajícího
        average_seller_rating = user.seller_reviews.aggregate(Avg('seller_rating'))['seller_rating__avg']

        return render(request, 'user_detail.html', {
            'user': user,
            'created_auctions': created_auctions,
            'bided_auctions': bided_auctions,
            'bought_auctions': bought_auctions,
            'average_buyer_rating': average_buyer_rating,
            'average_seller_rating': average_seller_rating
        })
    else:
        return HttpResponseForbidden("Nemáte oprávnění pro zobrazení detailů uživatele.")


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

        # Filtrace podle ceny Place bid
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

    return render(request, 'detailed_search.html', {'form': form, 'search': auctions})


from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import AddAuction, Bid, TransactionEvaluation

def auction_detail(request, pk):
    auction = get_object_or_404(AddAuction, pk=pk)

    # Zvýšení počtu zobrazení
    auction.number_of_views += 1
    auction.save()

    # Seřazení příhozů podle času, abychom je zobrazili chronologicky
    bids = Bid.objects.filter(auction=auction).order_by('-timestamp')

    # Získání posledního přihazujícího (pokud nějaký je)
    last_bider = bids.first().user if bids.exists() else None

    # Kontrola, zda aukce už vypršela
    auction_expired = auction.auction_end_date and auction.auction_end_date < timezone.now()

    if auction_expired:
        time_left = None
    else:
        # Výpočet zbývajícího času
        time_left = auction.auction_end_date - timezone.now()
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

    # Zjistíme, jestli je aktuální uživatel prodávající nebo kupující
    is_seller = request.user == auction.user_creator
    is_buyer = auction.name_buyer and request.user == auction.name_buyer  # Kontrola, jestli má aukce kupujícího
    can_add_evaluation = is_seller or is_buyer

    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Přesměrování na login s parametrem next
            return redirect(f'{reverse("login")}?next={request.path}')

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

            if auction.minimum_bid and new_bid < auction.minimum_bid:
                return render(request, 'add_auction_detail.html', {
                    'auction': auction,
                    'bids': bids,
                    'error_message': f'Your bid is lower than the minimum bid. Minimum bid is {auction.minimum_bid} Kč.'
                })

            if auction.price is None:
                auction.price = auction.start_price

            auction.previous_price = auction.price
            auction.price += new_bid

            Bid.objects.create(auction=auction, user=request.user, amount=new_bid, price=auction.price)
            auction.name_bider = request.user
            auction.save()

            return redirect('add_auction_detail', pk=auction.pk)

        else:
            return render(request, 'add_auction_detail.html', {
                'auction': auction,
                'bids': bids,
                'error_message': 'Musíte zadat částku příhozu.'
            })

    return render(request, 'add_auction_detail.html', {
        'auction': auction,
        'bids': bids,
        'last_bider': last_bider,
        'auction_expired': auction_expired,
        'days': days if not auction_expired else 0,
        'hours': hours if not auction_expired else 0,
        'minutes': minutes if not auction_expired else 0,
        'can_add_evaluation': can_add_evaluation,  # Předáme proměnnou pro kontrolu hodnocení
    })



def about_us(request):
    # Získání všech záznamů z modelu About
    about_entries = About.objects.all()
    page_name = 'About us'
    # Předání těchto dat do šablony
    return render(request, 'about_us.html', {
        'page_name': page_name,
        'about_entries': about_entries,
    })


def index(request):
    return render(request, template_name='base_4_obrazky.html', context={})
