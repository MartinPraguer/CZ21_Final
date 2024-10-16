# python manage.py runscript populate_data -v3

import time
import random
import os
from datetime import timedelta
from django.utils import timezone
from viewer.models import AddAuction, User, Category, Bid, AuctionImage
from django.core.files import File

# Nastavení cesty k adresáři s fotografiemi
PHOTO_DIR = 'media/photos/'  # Nahraďte touto cestou k vašemu adresáři s fotografiemi
SAVE_DIR = 'photos_add_auction/'  # Složka, kam se budou ukládat nové obrázky

# Seznam souborů fotografií z adresáře
photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif', '.png'))]

# Funkce pro vytvoření náhodných příhozů a nastavení kupujícího
def create_random_bids_and_buy_now(auction, users):
    if auction.auction_type == 'place_bid':
        num_bids = random.randint(5, 10)  # 5 až 10 náhodných příhozů
        current_price = auction.start_price  # Začínáme od počáteční ceny
        previous_price = None  # Proměnná pro uložení předchozí ceny

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
        auction.auction_end_date = timezone.now()  # Nastavíme aktuální čas jako konec aukce
        auction.save()

    elif auction.auction_type == 'buy_now':
        user = random.choice(users)
        auction.name_buyer = user  # Kupující je nastaven pouze pro aukce typu buy_now
        auction.is_sold = True
        auction.auction_end_date = timezone.now()  # Nastavíme aktuální čas jako konec aukce
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
            price = None
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
            price=price,
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

# Funkce `run()` jako vstupní bod skriptu
def run():
    # Vytvoření superuživatele
    if not User.objects.filter(username='1234').exists():
        User.objects.create_superuser(username='1234', password='1234', email='')

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
            price = None
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
            price=price,
            start_price=start_price,
            previous_price=None,
            minimum_bid=minimum_bid,
            auction_start_date=auction_start_date,
            auction_end_date=auction_end_date,
            number_of_views=random.randint(0, 1000),
            name_buyer=None  # Kupující je nastaven pouze pro aukce typu buy_now
        )

        add_auction.save()

        # Přidání obrázků k aukci
        add_auction_images(add_auction, categorized_photos[category])

        # Pokud je aukce typu 'place_bid', přidáme příhozy a nastavíme vítěze
        if auction_type == 'place_bid':
            create_random_bids_and_buy_now(add_auction, all_users)

        # Pokud je aukce typu 'buy_now', simulujeme nákup
        if auction_type == 'buy_now':
            create_random_bids_and_buy_now(add_auction, all_users)

        # Přidání krátkého zpoždění mezi generováním aukcí (např. 0,1 až 0,3 sekundy)
        time.sleep(random.uniform(0.1, 0.3))

    print("Data populated successfully!")