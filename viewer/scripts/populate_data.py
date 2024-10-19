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
                                                         defaults={'email': f'{username}@example.com',
                                                                   'password': '1234'})
        account_premium, _ = AccountType.objects.get_or_create(account_type='Premium')
        UserAccounts.objects.create(user=user, account_type=account_premium, is_premium=True)
        users.append(user)

    for username in user_nicks:
        user, created = user_model.objects.get_or_create(username=username,
                                                         defaults={'email': f'{username}@example.com',
                                                                   'password': '1234'})
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


# Funkce pro vytvoření aukcí bez příhozů
def create_auctions_without_bids(users, categories, auction_type, premium, expired, count, sample_names,
                                 sample_descriptions, categorized_photos):
    for _ in range(count):
        user = random.choice(users)
        category = random.choice(categories)
        name_auction = random.choice(sample_names[category.name])
        description = random.choice(sample_descriptions[category.name])
        start_price = random.randint(1000, 100000)
        auction_end_date = timezone.now() - timedelta(days=7) if expired else timezone.now() + timedelta(days=7)

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
            auction_start_date=timezone.now() - timedelta(days=random.randint(1, 7)),
            auction_end_date=auction_end_date,
            is_sold=False if auction_type == 'place_bid' else random.choice([True, False]),
            number_of_views=random.randint(0, 1000),
        )

        # Přidání obrázků k aukci
        add_auction_images(auction, categorized_photos[category.name])


# Funkce pro vytvoření aukcí s příhozy
def create_auctions_with_bids(users, categories, auction_type, premium, expired, count, sample_names,
                              sample_descriptions, categorized_photos):
    for _ in range(count):
        user = random.choice(users)
        category = random.choice(categories)
        name_auction = random.choice(sample_names[category.name])
        description = random.choice(sample_descriptions[category.name])
        start_price = random.randint(1000, 100000)
        auction_end_date = timezone.now() - timedelta(days=7) if expired else timezone.now() + timedelta(days=7)

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
            auction_start_date=timezone.now() - timedelta(days=random.randint(1, 7)),
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


# Funkce pro výpis počtu aukcí pro dané kategorie
def print_auction_counts():
    print(
        f"Buy now expired without bids: {AddAuction.objects.filter(auction_type='buy_now', is_sold=False, auction_end_date__lte=timezone.now()).count()}")
    print(
        f"Buy now expired with purchases: {AddAuction.objects.filter(auction_type='buy_now', is_sold=True, auction_end_date__lte=timezone.now()).count()}")
    print(
        f"Place bid premium expired without bids: {AddAuction.objects.filter(auction_type='place_bid', promotion=True, is_sold=False, auction_end_date__lte=timezone.now()).count()}")
    print(
        f"Place bid premium expired with purchases: {AddAuction.objects.filter(auction_type='place_bid', promotion=True, is_sold=True, auction_end_date__lte=timezone.now()).count()}")
    print(
        f"Place bid without premium expired without bids: {AddAuction.objects.filter(auction_type='place_bid', promotion=False, is_sold=False, auction_end_date__lte=timezone.now()).count()}")
    print(
        f"Place bid without premium expired with purchases: {AddAuction.objects.filter(auction_type='place_bid', promotion=False, is_sold=True, auction_end_date__lte=timezone.now()).count()}")
    print(
        f"Buy now active without bids: {AddAuction.objects.filter(auction_type='buy_now', auction_end_date__gt=timezone.now(), is_sold=False).count()}")
    print(
        f"Place bid premium active with bids: {AddAuction.objects.filter(auction_type='place_bid', promotion=True, auction_end_date__gt=timezone.now(), bids__isnull=False).count()}")
    print(
        f"Place bid without premium active with bids: {AddAuction.objects.filter(auction_type='place_bid', promotion=False, auction_end_date__gt=timezone.now(), bids__isnull=False).count()}")


# Hlavní funkce pro spuštění skriptu
def run():
    # Definování vzorků názvů a popisů pro aukce
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

    # Vytvoření kategorií a uživatelů
    categories = create_default_categories()
    users = create_default_users()

    # Vytvoření aukcí
    create_auctions_without_bids(users, categories, 'buy_now', 'without_premium', True, 5, sample_names,
                                 sample_descriptions, categorized_photos)
    create_auctions_with_bids(users, categories, 'buy_now', 'without_premium', True, 5, sample_names,
                              sample_descriptions, categorized_photos)
    create_auctions_without_bids(users, categories, 'place_bid', 'premium', True, 5, sample_names, sample_descriptions,
                                 categorized_photos)
    create_auctions_with_bids(users, categories, 'place_bid', 'premium', True, 5, sample_names, sample_descriptions,
                              categorized_photos)
    create_auctions_without_bids(users, categories, 'place_bid', 'without_premium', True, 5, sample_names,
                                 sample_descriptions, categorized_photos)
    create_auctions_with_bids(users, categories, 'place_bid', 'without_premium', True, 5, sample_names,
                              sample_descriptions, categorized_photos)
    create_auctions_without_bids(users, categories, 'buy_now', 'without_premium', False, 30, sample_names,
                                 sample_descriptions, categorized_photos)
    create_auctions_with_bids(users, categories, 'place_bid', 'premium', False, 30, sample_names, sample_descriptions,
                              categorized_photos)
    create_auctions_with_bids(users, categories, 'place_bid', 'without_premium', False, 30, sample_names,
                              sample_descriptions, categorized_photos)

    # Výpis počtu aukcí
    print_auction_counts()

