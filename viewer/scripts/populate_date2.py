from django.contrib.auth import get_user_model
from viewer.models import AddAuction, Bid, Category, UserAccounts, AccountType, AuctionImage, About
from django.utils import timezone
from datetime import timedelta
import random
import os
from django.core.files import File
from viewer.models import TransactionEvaluation

# Cesty k fotografiím
PHOTO_DIR = 'media/photos/'
SAVE_DIR = 'photos_add_auction/'

# Seznam souborů fotografií
photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif', '.png'))]

# Funkce pro vytvoření kategorií
def create_default_categories():
    categories = ['Paintings', 'Statues', 'Numismatics', 'Jewelry']
    category_objects = []
    for category_name in categories:
        category, created = Category.objects.get_or_create(name=category_name)
        category_objects.append(category)
    return category_objects

def get_or_create_user(username, email):
    user_model = get_user_model()  # Získáme model User (základní nebo rozšířený)
    user, created = user_model.objects.get_or_create(username=username, defaults={'email': email})

    # Pokud byl uživatel právě vytvořen, nastavíme mu výchozí heslo
    if created:
        user.set_password('1234')  # Můžeš změnit heslo na bezpečnější
        user.save()

    return user

# Funkce pro vytvoření uživatelů
def create_default_users():
    user_model = get_user_model()
    premium_nicks = ["SkylineWalker", "ThunderBlade", "MysticVoyager", "PixelCrafter", "ShadowHunter23", "NeonNinja",
                     "BlazeRunner", "1234"]
    user_nicks = ["FrozenPhoenix", "CyberSailor", "EchoJumper", "IronWolfX", "CosmicRider", "LunarKnight7",
                  "SwiftFalcon", "CrimsonEcho"]
    users = []

    superuser, created = user_model.objects.get_or_create(
        username='1234',
        defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
    )
    if created:
        superuser.set_password('1234')
        superuser.save()
    users.append(superuser)

    # Martin Praguer
    user = get_or_create_user(username='Martin Praguer', email='martin.praguer@gmail.com')
    if not About.objects.filter(about_user=user).exists():
        About.objects.create(
            photo='about_us/Martin Praguer.png',  # Cesta k obrázku
            about_user=user,
            contact='martin.praguer@gmail.com',
            locket1='Role in the project:',
            locket2='populate data',
            locket3='templates and details',
            locket4='',
            locket5='https://www.linkedin.com/in/martinpraguer/',
        )

    # Andrej Schön
    user = get_or_create_user(username='Andrej Schön', email='a.schon@seznam.cz')
    if not About.objects.filter(about_user=user).exists():
        About.objects.create(
            photo='about_us/Andrej Schön.jpg',
            about_user=user,
            contact='a.schon@seznam.cz',
            locket1='Role in the project:',
            locket2='account administration',
            locket3='shopping cart',
            locket4='',
            locket5='https://www.linkedin.com/in/andrej-sch%C3%B6n-032893333/',
        )

    # Ondřej Vitásek
    user = get_or_create_user(username='Ondřej Vitásek', email='ondrasek11vitasek@seznam.cz')
    if not About.objects.filter(about_user=user).exists():
        About.objects.create(
            photo='about_us/Ondřej Vitásek.jpg',
            about_user=user,
            contact='ondrasek11vitasek@seznam.cz',
            locket1='Role in the project:',
            locket2='morale boost',
            locket3='tester',
            locket4='',
            locket5='',
        )

    for username in premium_nicks:
        if username == '1234':
            continue
        user, created = user_model.objects.get_or_create(username=username,
                                                         defaults={'email': f'{username}@example.com'})
        if created:
            user.set_password('1234')
            user.save()
        account_premium, _ = AccountType.objects.get_or_create(account_type='Premium')
        UserAccounts.objects.create(user=user, account_type=account_premium, is_premium=True)
        users.append(user)

    for username in user_nicks:
        user, created = user_model.objects.get_or_create(username=username,
                                                         defaults={'email': f'{username}@example.com'})
        if created:
            user.set_password('1234')
            user.save()
        users.append(user)
    return users

# Funkce pro přidání obrázků k aukci
def add_auction_images(auction, category_photos):
    num_images = random.randint(1, 3)
    selected_photos = random.sample(category_photos, num_images)
    for photo in selected_photos:
        photo_path = os.path.join(PHOTO_DIR, photo)
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo_file:
                auction_image = AuctionImage(auction=auction)
                auction_image.image.save(os.path.join(SAVE_DIR, photo), File(photo_file), save=True)

# Funkce pro generování startu a konce aukce
def generate_auction_dates(expired):
    if expired:
        start_date = timezone.now() - timedelta(days=random.randint(7, 14))
    else:
        start_date = timezone.now() - timedelta(days=random.randint(0, 6))
    end_date = start_date + timedelta(days=7)
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
        auction_start_date, auction_end_date = generate_auction_dates(expired)

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
        add_auction_images(auction, categorized_photos[category.name])

# Funkce pro vytvoření aukcí s příhozy nebo zakoupenými (sold)
def create_auctions_with_bids(users, categories, auction_type, premium, expired, count, sample_names,
                              sample_descriptions, categorized_photos):
    for _ in range(count):
        user = random.choice(users)
        category = random.choice(categories)
        name_auction = random.choice(sample_names[category.name])
        description = random.choice(sample_descriptions[category.name])
        start_price = random.randint(1000, 100000)
        auction_start_date, auction_end_date = generate_auction_dates(expired)

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
        add_auction_images(auction, categorized_photos[category.name])

        # Pokud je aukce typu 'buy_now', nastavíme kupujícího
        if auction_type == 'buy_now':
            auction.name_buyer = random.choice(users)  # Nastavíme kupujícího pro 'Buy Now' aukci
            auction.is_sold = True
            auction.save()

            # Generování hodnocení mezi prodávajícím a kupujícím pro 'Buy Now' aukce, pokud je aukce skončená
            if expired:
                generate_evaluation(auction, auction.user_creator, auction.name_buyer)

        # Pokud je aukce typu 'place_bid', přidáme příhozy
        elif auction_type == 'place_bid':
            current_price = start_price
            num_bids = random.randint(1, 10)
            last_bidder = None  # Proměnná pro uchování posledního přihazujícího

            for _ in range(num_bids):
                bidder = random.choice(users)
                last_bidder = bidder  # Uložení posledního přihazujícího
                min_bid_increment = auction.minimum_bid
                bid_amount = random.randint(min_bid_increment, min_bid_increment + 2000)
                auction.previous_price = current_price
                current_price += bid_amount
                Bid.objects.create(
                    auction=auction,
                    user=bidder,
                    amount=bid_amount,
                    price=current_price,
                    timestamp=timezone.now()
                )

            # Pokud aukce již vypršela, poslední přihazující se stane kupujícím
            if expired and last_bidder:
                auction.name_buyer = last_bidder
                auction.is_sold = True
                auction.save()

                # Generování hodnocení mezi prodávajícím a kupujícím, pokud je aukce skončená
                generate_evaluation(auction, auction.user_creator, auction.name_buyer)

            # Pokud aukce ještě nevypršela, označ posledního přihazujícího jako name_bider
            elif not expired and last_bidder:
                auction.name_bider = last_bidder

            auction.price = current_price
            auction.save()

def generate_evaluation(auction, seller, buyer):
    """Funkce pro generování vzájemného hodnocení mezi prodávajícím a kupujícím."""
    seller_rating = random.randint(1, 5)
    buyer_rating = random.randint(1, 5)

    # Komentáře pro prodávajícího a kupujícího
    seller_comments = [
        "The buyer was very prompt and polite.",
        "Smooth transaction, would recommend.",
        "Quick payment, easy communication."
    ]
    buyer_comments = [
        "The item was as described, fast delivery.",
        "Seller was very professional and helpful.",
        "Great experience, would buy again!"
    ]

    # Vytvoření hodnocení
    TransactionEvaluation.objects.create(
        auction=auction,
        seller=seller,
        buyer=buyer,
        seller_rating=seller_rating,
        buyer_rating=buyer_rating,
        seller_comment=random.choice(seller_comments),
        buyer_comment=random.choice(buyer_comments),
    )

# Hlavní funkce pro spuštění skriptu
def run():
    sample_descriptions = {
        'Paintings': ["A beautiful piece of art from the 18th century.",
                      "An exquisite oil painting with vibrant colors."],
        'Statues': ["A stunning ancient statue with a rich history.", "A captivating bronze sculpture."],
        'Numismatics': ["Rare coins from the medieval era.", "Silver and gold coins dating back to the Roman Empire."],
        'Jewelry': ["Elegant and unique piece of jewelry, perfect for collectors.",
                    "A dazzling emerald ring set in gold."]
    }

    sample_names = {
        'Paintings': ["Classic Painting", "Sunset Portrait"],
        'Statues': ["Ancient Statue", "Mythical Creature"],
        'Numismatics': ["Golden Coin", "Silver Coin Set"],
        'Jewelry': ["Ruby Necklace", "Emerald Ring"]
    }

    categorized_photos = {
        'Paintings': [f for f in photos if f.startswith('obraz')],
        'Statues': [f for f in photos if f.startswith('socha')],
        'Numismatics': [f for f in photos if f.startswith('mince')],
        'Jewelry': [f for f in photos if f.startswith('šperk')]
    }

    categories = create_default_categories()
    users = create_default_users()

    # Expirované aukce (14-7 dní zpět)
    create_auctions_without_bids(users, categories, 'buy_now', 'without_premium', True, 5, sample_names,
                                 sample_descriptions, categorized_photos)  # not sold
    create_auctions_with_bids(users, categories, 'buy_now', 'without_premium', True, 5, sample_names,
                              sample_descriptions, categorized_photos)  # sold

    create_auctions_without_bids(users, categories, 'place_bid', 'premium', True, 5, sample_names, sample_descriptions,
                                 categorized_photos)  # not sold
    create_auctions_with_bids(users, categories, 'place_bid', 'premium', True, 5, sample_names, sample_descriptions,
                              categorized_photos)  # sold

    create_auctions_without_bids(users, categories, 'place_bid', 'without_premium', True, 5, sample_names,
                                 sample_descriptions, categorized_photos)  # not sold
    create_auctions_with_bids(users, categories, 'place_bid', 'without_premium', True, 5, sample_names,
                              sample_descriptions, categorized_photos)  # sold

    # Aktivní aukce (méně než 7 dní zpět)
    create_auctions_without_bids(users, categories, 'buy_now', 'without_premium', False, 30, sample_names,
                                 sample_descriptions, categorized_photos)  # active without bids
    create_auctions_with_bids(users, categories, 'place_bid', 'premium', False, 30, sample_names, sample_descriptions,
                              categorized_photos)  # active with bids promotion
    create_auctions_with_bids(users, categories, 'place_bid', 'without_premium', False, 30, sample_names,
                              sample_descriptions, categorized_photos)  # active without bids

run()