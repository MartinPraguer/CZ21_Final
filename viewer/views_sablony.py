from viewer.views import *















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
    return render(request, template_name='4+3_kategorie.html', context={
        'page_name': 'Auction Archives',  # Předání názvu stránky
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj,
        'current_time': current_time,
    })


def current_auctions(request):
    # Získání aktuálního času
    current_time = timezone.now()

    # Přesun aukcí, kterým vypršel čas, do archivovaných, pokud nejsou prodané
    expired_auctions = AddAuction.objects.filter(auction_end_date__lte=current_time, is_sold=False)

    for auction in expired_auctions:
        # Zkontrolujeme, zda aukce má kupujícího a cenu, než ji přesuneme do archivovaných nákupů
        if auction.name_buyer and auction.price is not None:
            # Pokud aukce není v archivu, přesuneme ji
            if not ArchivedPurchase.objects.filter(auction=auction).exists():
                ArchivedPurchase.objects.create(
                    user=auction.name_buyer,  # Zde se uloží uživatel jako kupující
                    auction=auction,
                    price=auction.price  # Cena aukce
                )
        # Označíme aukci jako prodanou
        auction.is_sold = True
        auction.save()

    # Filtrujte pouze inzeráty s aukcemi typu "Buy Now", které ještě neskončily
    buy_now_add_auction = AddAuction.objects.filter(
        auction_type='buy_now',
        auction_end_date__gt=current_time  # Aukce, které ještě neskončily
    ).order_by("auction_end_date")

    # Aukce s propagací, které nejsou "Buy Now", a ještě neskončily
    promotion_add_auction = AddAuction.objects.filter(
        promotion=True,
        auction_type='place_bid',
        auction_end_date__gt=current_time  # Aukce, které ještě neskončily
    ).order_by("auction_end_date")

    # Aukce bez propagace, které nejsou "Buy Now", a ještě neskončily
    no_promotion_add_auction = AddAuction.objects.filter(
        promotion=False,
        auction_type='place_bid',
        auction_end_date__gt=current_time  # Aukce, které ještě neskončily
    ).order_by("auction_end_date")

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
            if auction.auction_end_date and auction.auction_end_date > current_time:
                time_left = auction.auction_end_date - current_time
                auction.days_left = time_left.days
                auction.hours_left, remainder = divmod(time_left.seconds, 3600)
                auction.minutes_left, _ = divmod(remainder, 60)
            else:
                auction.days_left = auction.hours_left = auction.minutes_left = 0

    # Předejte název stránky
    return render(request, template_name='4+3_kategorie.html', context={
        'page_name': 'Current Auctions',  # Předání názvu stránky
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })


def last_auction(request):
    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte všechny aukce typu "Buy Now", které ještě neskončily
    buy_now_add_auction = AddAuction.objects.filter(
        auction_type='buy_now',
        auction_end_date__gt=current_time  # Aukce, které ještě neskončily
    ).order_by("-created")  # Seřazeno podle data vytvoření, nejnovější první

    # Filtrujte aukce s propagací, které nejsou "Buy Now"
    promotion_add_auction = AddAuction.objects.filter(
        promotion=True,
        auction_type='place_bid',
        auction_end_date__gt=current_time
    ).order_by("-created")

    # Filtrujte aukce bez propagace, které nejsou "Buy Now"
    no_promotion_add_auction = AddAuction.objects.filter(
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

    # Vykreslení šablony s aukcemi
    return render(request, template_name='4+3_kategorie.html', context={
        'page_name': 'Last auction',
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })




def paintings(request):
    # Získání kategorie "Paintings"
    paintings_category = Category.objects.get(name="Paintings")

    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte pouze inzeráty s kategorií "Paintings" a aukcemi typu "Buy Now", které ještě neskončily
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

    return render(request, template_name='4+3_kategorie.html', context={
        'page_name': 'Paintings',
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })


def statues(request):
    # Získání kategorie "statues"
    statues_category = Category.objects.get(name="Statues")

    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte pouze inzeráty s kategorií "Statues" a aukcemi typu "Buy Now", které ještě neskončily
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

    return render(request, template_name='4+3_kategorie.html', context={
        'page_name': 'Statues',
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })

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

    return render(request, template_name='4+3_kategorie.html', context={
        'page_name': 'Jewelry',
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })


def numismatics(request):
    # Získání kategorie "Numismatics"
    numismatics_category = Category.objects.get(name="Numismatics")

    # Získání aktuálního času
    current_time = timezone.now()

    # Filtrujte pouze inzeráty s kategorií "Numismatics" a aukcemi typu "Buy Now", které ještě neskončily
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

    return render(request, template_name='4+3_kategorie.html', context={
        'page_name': 'Numismatics',
        'buy_now_page_obj': buy_now_page_obj,
        'promotion_page_obj': promotion_page_obj,
        'no_promotion_page_obj': no_promotion_page_obj
    })