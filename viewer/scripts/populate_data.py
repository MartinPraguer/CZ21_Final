# python manage.py runscript populate_data -v3

import random
import os
from datetime import timedelta
from django.utils import timezone
from viewer.models import AddAuction, User, Category, Bid
from django.core.files import File

# Nastavení cesty k adresáři s fotografiemi
PHOTO_DIR = 'media/photos/'  # Nahraďte touto cestou k vašemu adresáři s fotografiemi
SAVE_DIR = 'photos_add_auction/'  # Složka, kam se budou ukládat nové obrázky

# Seznam souborů fotografií z adresáře
photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif', '.png'))]

# Funkce pro generování náhodného data začátku a konce aukce
def random_auction_dates():
    auction_start_date = timezone.now()
    random_days = random.randint(0, 20)  # Rozmezí 0-20 dní pro aukce
    auction_end_date = auction_start_date + timedelta(days=random_days)
    return auction_start_date, auction_end_date

# Funkce pro vytvoření náhodných příhozů (5-10) a nákupy pomocí Buy Now
def create_random_bids_and_buy_now(auction, users):
    if auction.auction_type == 'place_bid':
        num_bids = random.randint(5, 10)  # 5 až 10 náhodných příhozů
        for _ in range(num_bids):
            user = random.choice(users)
            bid_amount = auction.start_price + random.randint(100, 1000)  # Náhodný příhoz
            Bid.objects.create(auction=auction, user=user, amount=bid_amount)
            auction.name_bider = user  # Nastavení posledního přihazujícího
            auction.price = bid_amount  # Aktualizace ceny
            auction.save()
    elif auction.auction_type == 'buy_now':
        user = random.choice(users)
        auction.name_buyer = user  # Uživatelem zakoupeno
        auction.save()

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

    for _ in range(100):
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
            previous_price = None
            minimum_bid = random.randint(500, 1000)

        promotion = random.choice([True, False])
        auction_start_date, auction_end_date = random_auction_dates()
        number_of_views = random.randint(0, 1000)

        if categorized_photos[category]:
            random_photo = random.choice(categorized_photos[category])
            photo_path = os.path.join(PHOTO_DIR, random_photo)

            add_auction = AddAuction(
                user_creater=user,
                category=all_categories[category],
                name_auction=name_auction,
                description=description,
                promotion=promotion,
                auction_type=auction_type,
                buy_now_price=buy_now_price,
                price=price,
                start_price=start_price,
                previous_price=previous_price,
                minimum_bid=minimum_bid,
                auction_start_date=auction_start_date,
                auction_end_date=auction_end_date,
                number_of_views=number_of_views,
            )

            if os.path.exists(photo_path):
                with open(photo_path, 'rb') as photo_file:
                    add_auction.photo.save(os.path.join(SAVE_DIR, random_photo), File(photo_file), save=True)

            add_auction.save()

            # Vytvoření náhodných příhozů a nákupu "Buy Now"
            create_random_bids_and_buy_now(add_auction, all_users)

    print("Data populated successfully!")
