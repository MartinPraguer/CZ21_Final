# python manage.py runscript populate_data -v3

from django.contrib.auth import get_user_model
from viewer.models import AddAuction, Bid, Category, UserAccounts, AccountType, AuctionImage, About
from django.utils import timezone
from datetime import timedelta
import random
import os
from django.core.files import File

# Cesty k fotografiím
PHOTO_DIR = 'media/photos/'  # Cesta k adresáři s fotografiemi
SAVE_DIR = 'photos_add_auction/'  # Cesta k uložení obrázků

# Seznam souborů fotografií
photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif', '.png'))]


# Funkce pro vytvoření kategorií, pokud neexistují
def create_default_categories():
    categories = ['Paintings', 'Statues', 'Numismatics', 'Jewelry']
    category_objects = []
    for category_name in categories:
        category, created = Category.objects.get_or_create(name=category_name)
        category_objects.append(category)
    return category_objects


# Funkce pro vytvoření uživatelů
def create_default_users():
    user_model = get_user_model()

    premium_nicks = ["SkylineWalker", "ThunderBlade", "MysticVoyager", "PixelCrafter", "ShadowHunter23", "NeonNinja",
                     "BlazeRunner", "1234"]
    user_nicks = ["FrozenPhoenix", "CyberSailor", "EchoJumper", "IronWolfX", "CosmicRider", "LunarKnight7",
                  "SwiftFalcon", "CrimsonEcho"]

    users = []
    for username in premium_nicks:
        user, created = user_model.objects.get_or_create(username=username,
                                                         defaults={'email': f'{username}@example.com'})
        if created:
            user.set_password('1234')  # Nastavení šifrovaného hesla
            user.save()

        account_premium, _ = AccountType.objects.get_or_create(account_type='Premium')
        UserAccounts.objects.create(user=user, account_type=account_premium, is_premium=True)
        users.append(user)

    for username in user_nicks:
        user, created = user_model.objects.get_or_create(username=username,
                                                         defaults={'email': f'{username}@example.com'})
        if created:
            user.set_password('1234')  # Nastavení šifrovaného hesla
            user.save()

        users.append(user)
    return users


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


# Funkce pro generování startu a konce aukce
def generate_auction_dates(expired):
    if expired:
        # Pokud aukce expirovala, start je náhodně mezi 7 a 14 dny zpět, trvání 7 dnů
        start_date = timezone.now() - timedelta(days=random.randint(7, 14))
    else:
        # Pokud aukce neexpirovala, start je méně než 7 dní před aktuálním časem, trvání 7 dnů
        start_date = timezone.now() - timedelta(days=random.randint(0, 6))

    end_date = start_date + timedelta(days=7)  # Aukce trvá vždy 7 dní
    return start_date, end_date


# Funkce pro vytvoření aukcí bez příhozů (not sold)
def create_auctions_without_bids(users, categories, auction_type, premium, expired, count, sample_names,
                                 sample_descriptions, categorized_photos):
    for _ in range(count):
        user = random.choice(users)
        category = random.choice(categories)
        name_auction = random.choice(sample_names[category.name])
        description = random.choice(sample_descriptions[category.name])
        start_price = random.randint(1000, 100000)
        auction_start_date, auction_end_date = generate_auction_dates(
            expired)  # Použití funkce pro nastavení startu a konce aukce

        auction = AddAuction.objects.create(
            user_creator=user,
            category=category,
            name_auction=name_auction,
            description=description,
            auction_type=auction_type,
            price=start_price if auction_type == 'place_bid' else None,
            start_price=start_price if auction_type == 'place_bid' else None,
            buy_now_price=random.randint(1000, 100000) if auction_type == 'buy_now' else None,
            minimum_bid=random.randint(500, 1000) if auction_type == 'place_bid' else None,
            promotion=(premium == 'premium'),
            auction_start_date=auction_start_date,
            auction_end_date=auction_end_date,
            is_sold=False,
            number_of_views=random.randint(0, 1000),
        )

        # Přidání obrázků k aukci
        add_auction_images(auction, categorized_photos[category.name])


# Funkce pro vytvoření aukcí s příhozy (sold)
def create_auctions_with_bids(users, categories, auction_type, premium, expired, count, sample_names,
                              sample_descriptions, categorized_photos):
    for _ in range(count):
        user = random.choice(users)
        category = random.choice(categories)
        name_auction = random.choice(sample_names[category.name])
        description = random.choice(sample_descriptions[category.name])
        start_price = random.randint(1000, 100000)
        auction_start_date, auction_end_date = generate_auction_dates(
            expired)  # Použití funkce pro nastavení startu a konce aukce

        auction = AddAuction.objects.create(
            user_creator=user,
            category=category,
            name_auction=name_auction,
            description=description,
            auction_type=auction_type,
            price=start_price if auction_type == 'place_bid' else None,
            start_price=start_price if auction_type == 'place_bid' else None,
            buy_now_price=random.randint(1000, 100000) if auction_type == 'buy_now' else None,
            minimum_bid=random.randint(500, 1000) if auction_type == 'place_bid' else None,
            promotion=(premium == 'premium'),
            auction_start_date=auction_start_date,
            auction_end_date=auction_end_date,
            is_sold=True,
            number_of_views=random.randint(0, 1000),
        )

        # Přidání obrázků k aukci
        add_auction_images(auction, categorized_photos[category.name])

        # Pokud aukce má příhozy (platí pro 'place_bid')
        if auction_type == 'place_bid':
            current_price = start_price
            num_bids = random.randint(1, 10)
            for _ in range(num_bids):
                bidder = random.choice(users)
                bid_amount = random.randint(500, 2000)
                current_price += bid_amount
                Bid.objects.create(
                    auction=auction,
                    user=bidder,
                    amount=bid_amount,
                    price=current_price,
                    timestamp=timezone.now()
                )
            auction.price = current_price
            auction.save()


# Hlavní funkce pro spuštění skriptu
def run():
    sample_descriptions = {
        'Paintings': ["A beautiful piece of art from the 18th century.",
                      "An exquisite oil painting with vibrant colors.",
                      "A charming landscape painting with rich details."],
        'Statues': ["A stunning ancient statue with a rich history.",
                    "A finely crafted marble statue from the Renaissance.", "A captivating bronze sculpture."],
        'Numismatics': ["Rare coins from the medieval era.",
                        "A collection of ancient coins with historical significance.",
                        "Silver and gold coins dating back to the Roman Empire."],
        'Jewelry': ["Elegant and unique piece of jewelry, perfect for collectors.",
                    "A dazzling emerald ring set in gold.", "A delicate diamond necklace with intricate design."]
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

    categories = create_default_categories()
    users = create_default_users()

    # Expirované buy now aukce
    create_auctions_without_bids(users, categories, 'buy_now', 'without_premium', True, 5, sample_names,
                                 sample_descriptions, categorized_photos)  # not sold
    create_auctions_with_bids(users, categories, 'buy_now', 'without_premium', True, 5, sample_names,
                              sample_descriptions, categorized_photos)  # sold

    # Expirované place bid promotion aukce
    create_auctions_without_bids(users, categories, 'place_bid', 'premium', True, 5, sample_names, sample_descriptions,
                                 categorized_photos)  # not sold
    create_auctions_with_bids(users, categories, 'place_bid', 'premium', True, 5, sample_names, sample_descriptions,
                              categorized_photos)  # sold

    # Expirované place bid without promotion aukce
    create_auctions_without_bids(users, categories, 'place_bid', 'without_premium', True, 5, sample_names,
                                 sample_descriptions, categorized_photos)  # not sold
    create_auctions_with_bids(users, categories, 'place_bid', 'without_premium', True, 5, sample_names,
                              sample_descriptions, categorized_photos)  # sold

    # Aktivní buy now aukce
    create_auctions_without_bids(users, categories, 'buy_now', 'without_premium', False, 30, sample_names,
                                 sample_descriptions, categorized_photos)  # active without bids

    # Aktivní place bid promotion aukce
    create_auctions_with_bids(users, categories, 'place_bid', 'premium', False, 30, sample_names, sample_descriptions,
                              categorized_photos)  # active with bids (promotion)

    # Aktivní place bid without promotion aukce
    create_auctions_with_bids(users, categories, 'place_bid', 'without_premium', False, 30, sample_names,
                              sample_descriptions, categorized_photos)  # active with bids (without promotion)
