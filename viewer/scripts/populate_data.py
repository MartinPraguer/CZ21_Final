# python manage.py runscript populate_data -v3

from django.contrib.auth import get_user_model
from viewer.models import UserAccounts, AccountType
import time
import random
import os
from datetime import timedelta
from django.utils import timezone
from viewer.models import AddAuction, User, Category, Bid, AuctionImage, About
from django.core.files import File

# Nastavení cesty k adresáři s fotografiemi
PHOTO_DIR = 'media/photos/'  # Nahraďte touto cestou k vašemu adresáři s fotografiemi
SAVE_DIR = 'photos_add_auction/'  # Složka, kam se budou ukládat nové obrázky

# Seznam souborů fotografií z adresáře
photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif', '.png'))]

# Funkce pro vytvoření náhodných příhozů a nastavení kupujícího
def create_random_bids_and_buy_now(auction, users):
    if auction.auction_type == 'place_bid':
        num_bids = random.randint(0, 10)  # Může být 0 příhozů, čímž aukce není prodána
        current_price = auction.start_price  # Začínáme od počáteční ceny
        previous_price = None  # Proměnná pro uložení předchozí ceny

        if num_bids > 0:
            for _ in range(num_bids):
                user = random.choice(users)

                # Přidáme minimální příhoz (minimum_bid) k aktuální ceně a k tomu náhodné zvýšení
                bid_increment = random.randint(auction.minimum_bid, auction.minimum_bid + 1000)
                current_price += bid_increment  # Nová celková cena po příhozu

                # Uložíme aktuální cenu jako nový příhoz
                Bid.objects.create(
                    auction=auction,
                    user=user,
                    amount=bid_increment,
                    price=current_price,  # Nastavení ceny po příhozu
                    timestamp=timezone.now()  # Přidání času příhozu
                )

                # Aktualizujeme aukci: nastavíme novou cenu a posledního přihazujícího
                auction.name_bider = user
                auction.price = current_price  # Nastavení nové aktuální ceny
                auction.previous_price = previous_price  # Nastavení přeškrtnuté ceny (předchozí cena)
                auction.save()

                # Uložíme aktuální cenu jako předchozí pro další příhoz
                previous_price = auction.price

            # Po skončení aukce nastavíme vítěze (poslední přihazující) jako kupujícího
            auction.name_buyer = auction.name_bider
            auction.is_sold = True
        else:
            # Pokud nebyly žádné příhozy, aukce není prodána
            auction.is_sold = False

        auction.auction_end_date = timezone.now()  # Nastavíme aktuální čas jako konec aukce
        auction.save()

    elif auction.auction_type == 'buy_now':
        # Náhodně rozhodneme, zda byla aukce zakoupena, nebo ne
        if random.choice([True, False]):
            user = random.choice(users)
            auction.name_buyer = user  # Kupující je nastaven pouze pro aukce typu buy_now
            auction.is_sold = True
            auction.auction_end_date = timezone.now()  # Nastavíme aktuální čas jako konec aukce
        else:
            auction.is_sold = False  # Pokud není náhodně zakoupeno, aukce není prodána
        auction.save()

# Funkce pro přidání více obrázků k aukci
def add_auction_images(auction, category_photos):
    num_images = random.randint(1, 1)  # Přidáme 1 obrázek pro každou aukci
    selected_photos = random.sample(category_photos, num_images)  # Náhodný výběr obrázků z kategorie

    for photo in selected_photos:
        photo_path = os.path.join(PHOTO_DIR, photo)
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo_file:
                auction_image = AuctionImage(auction=auction)
                auction_image.image.save(os.path.join(SAVE_DIR, photo), File(photo_file), save=True)

# Funkce pro vytvoření aukcí, které expirují bez příhozů
def create_expired_auctions_without_bids(users, categories, sample_names, sample_descriptions, categorized_photos):
    expired_auctions_count = 10
    for _ in range(expired_auctions_count):
        auction_type = random.choice(['place_bid', 'buy_now'])

        user = random.choice(users)
        category = random.choice(list(categories.keys()))
        name_auction = random.choice(sample_names[category])
        description = random.choice(sample_descriptions[category])

        if auction_type == 'buy_now':
            buy_now_price = random.randint(1000, 100000)
            price = buy_now_price  # Nastavíme cenu rovnou hodnotě buy_now_price
            start_price = None
            minimum_bid = None
        else:
            buy_now_price = None
            start_price = random.randint(1000, 100000)
            price = start_price
            minimum_bid = random.randint(500, 1000)

        # Aukce začala před 7 dny
        auction_start_date = timezone.now() - timedelta(days=7)
        # Aukce vyprší dnes, ale nemá žádné příhozy
        auction_end_date = auction_start_date + timedelta(days=7)

        # Vytvoření aukce
        expired_auction = AddAuction(
            user_creator=user,
            category=categories[category],
            name_auction=name_auction,
            description=description,
            promotion=random.choice([True, False]),
            auction_type=auction_type,
            buy_now_price=buy_now_price,
            price=price if price is not None else 0,  # Zajistíme, že cena nebude None
            start_price=start_price,
            previous_price=None,
            minimum_bid=minimum_bid,
            auction_start_date=auction_start_date,
            auction_end_date=auction_end_date,
            number_of_views=random.randint(0, 1000),
            is_sold=False  # Aukce není prodaná, protože neproběhly žádné příhozy
        )
        expired_auction.save()

        # Přidání obrázků k aukci
        add_auction_images(expired_auction, categorized_photos[category])

    print(f"{expired_auctions_count} expired auctions without bids created.")


def get_or_create_user(username, email, password='heslo123'):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return User.objects.create_user(username=username, email=email, password=password)


# Funkce `run()` jako vstupní bod skriptu
def run():
    if not User.objects.filter(username='1234').exists():
        # Vytvoření superuživatele
        superuser = User.objects.create_superuser(username='1234', password='1234', email='')

        # Získání typu účtu 'premium'
        # account_premium = AccountType.objects.get(name='premium')
        account_premium, created = AccountType.objects.get_or_create(account_type='Premium')
        premium_user_account = UserAccounts.objects.create(
            user=superuser,
            account_type=account_premium,
            is_premium=True,
            premium_expiry_date=timezone.now() + timedelta(days=30)
        )

        # Výstup pro kontrolu
        print(
            f"Prémiový účet vytvořen: {premium_user_account.is_premium}, Expirace: {premium_user_account.premium_expiry_date}")

    # Martin Praguer
    user = get_or_create_user(username='Martin Praguer', email='martin.praguer@gmail.com')
    if not About.objects.filter(about_user=user).exists():
        About.objects.create(
            photo='about/Martin Praguer.png',  # Cesta k obrázku
            about_user=user,
            contact = 'martin.praguer@gmail.com',
            locket1 = 'Role in the project:',
            locket2 = 'populate data',
            locket3 = 'templates and details',
            locket4 = '',
            locket5 = '',
        )

    # Andrej Schön
    user = get_or_create_user(username='Andrej Schön', email='a.schon@seznam.cz')
    if not About.objects.filter(about_user=user).exists():
        About.objects.create(
            photo='about/Andrej Schön.jpg',
            about_user=user,
            contact = 'a.schon@seznam.cz',
            locket1 = 'Role in the project:',
            locket2 = 'account administration',
            locket3 = 'shopping cart',
            locket4 = '',
            locket5 = '',
        )

    # Ondřej Vitásek
    user = get_or_create_user(username='Ondřej Vitásek', email='ondrasek11vitasek@seznam.cz')
    if not About.objects.filter(about_user=user).exists():
        About.objects.create(
            photo='about/Ondřej Vitásek.jpg',
            about_user=user,
            contact = 'ondrasek11vitasek@seznam.cz',
            locket1 = 'Role in the project:',
            locket2 = 'morale boost',
            locket3 = 'tester',
            locket4 = '',
            locket5 = '',
        )

    categories = ['Paintings', 'Statues', 'Numismatics', 'Jewelry']

    sample_descriptions = {
        'Paintings': [
            "A beautiful piece of art from the 18th century.",
            "An exquisite oil painting with vibrant colors.",
            "A charming landscape painting with rich details."
        ],
        'Statues': [
            "A stunning ancient statue with a rich history.",
            "A finely crafted marble statue from the Renaissance.",
            "A captivating bronze sculpture."
        ],
        'Numismatics': [
            "Rare coins from the medieval era.",
            "A collection of ancient coins with historical significance.",
            "Silver and gold coins dating back to the Roman Empire."
        ],
        'Jewelry': [
            "Elegant and unique piece of jewelry, perfect for collectors.",
            "A dazzling emerald ring set in gold.",
            "A delicate diamond necklace with intricate design."
        ]
    }

    sample_names = {
        'Paintings': ["Classic Painting", "Sunset Portrait", "Charming Landscape"],
        'Statues': ["Ancient Statue", "Mythical Creature", "Marble Bust"],
        'Numismatics': ["Golden Coin", "Silver Coin Set", "Rare Ancient Coin"],
        'Jewelry': ["Ruby Necklace", "Emerald Ring", "Diamond Earrings"]
    }

    categorized_photos = {
        'Paintings': [f for f in photos if f.startswith('obraz')],
        'Statues': [f for f in photos if f.startswith('socha')],
        'Numismatics': [f for f in photos if f.startswith('mince')],
        'Jewelry': [f for f in photos if f.startswith('šperk')]
    }

    user_nicks = [
        "SkylineWalker", "ThunderBlade", "MysticVoyager", "PixelCrafter", "ShadowHunter23",
        "NeonNinja", "BlazeRunner", "FrozenPhoenix", "CyberSailor", "EchoJumper",
        "IronWolfX", "CosmicRider", "LunarKnight7", "SwiftFalcon", "CrimsonEcho"
    ]

    all_users = [User.objects.get_or_create(username=nick)[0] for nick in user_nicks]
    all_categories = {cat: Category.objects.get_or_create(name=cat)[0] for cat in categories}

    # Vytvoření 10 aukcí, které expirují bez příhozů
    create_expired_auctions_without_bids(all_users, all_categories, sample_names, sample_descriptions, categorized_photos)

    for i in range(90):  # Zbytek z celkového počtu 100 aukcí
        user = random.choice(all_users)
        category = random.choice(categories)
        name_auction = random.choice(sample_names[category])
        description = random.choice(sample_descriptions[category])

        auction_type = random.choice(['buy_now', 'place_bid'])

        if auction_type == 'buy_now':
            buy_now_price = random.randint(1000, 100000)
            price = buy_now_price  # Pro buy_now nastavíme cenu rovnou buy_now_price
            start_price = None
            previous_price = None
            minimum_bid = None
        else:
            buy_now_price = None
            start_price = random.randint(1000, 100000)
            price = start_price
            minimum_bid = random.randint(500, 1000)

        promotion = random.choice([True, False])

        # Nastavení začátku aukce mezi -30 a +7 dny od teď
        auction_start_date = timezone.now() + timedelta(days=random.randint(-7, 7))

        # Trvání aukce bude 7 dnů
        auction_end_date = auction_start_date + timedelta(days=7)

        add_auction = AddAuction(
            user_creator=user,
            category=all_categories[category],
            name_auction=name_auction,
            description=description,
            promotion=promotion,
            auction_type=auction_type,
            buy_now_price=buy_now_price,
            price=price if price is not None else 0,  # Zajistíme, že cena nebude None
            start_price=start_price,
            previous_price=None,
            minimum_bid=minimum_bid,
            auction_start_date=auction_start_date,
            auction_end_date=auction_end_date,
            number_of_views=random.randint(0, 1000),
            name_buyer=None,  # Kupující je nastaven pouze pro aukce typu buy_now
            is_sold=False  # Nové aukce nejsou rovnou prodané
        )

        add_auction.save()

        # Přidání obrázků k aukci
        add_auction_images(add_auction, categorized_photos[category])

        # Pokud je aukce typu 'place_bid', přidáme příhozy
        if auction_type == 'place_bid':
            create_random_bids_and_buy_now(add_auction, all_users)

        # Pokud je aukce typu 'buy_now', simulujeme nákup
        if auction_type == 'buy_now':
            create_random_bids_and_buy_now(add_auction, all_users)

        # Přidání krátkého zpoždění mezi generováním aukcí (např. 0,1 až 0,3 sekundy)
        time.sleep(random.uniform(0.1, 0.3))

    print("Data populated successfully!")
