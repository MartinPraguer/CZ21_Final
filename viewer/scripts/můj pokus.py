from viewer.models import (UserAccounts, AccountType, AddAuction, User, Category, Bid, AuctionImage, About)
from django.utils import timezone
from django.core.files import File
from datetime import timedelta
import random
import os




PHOTO_DIR = 'media/photos/'
SAVE_DIR = 'photos_add_auction/'

# Získání seznamu fotografií
photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif', '.png'))]

categorized_photos = {
    'Paintings': [f for f in photos if f.startswith('obraz')],
    'Statues': [f for f in photos if f.startswith('socha')],
    'Numismatics': [f for f in photos if f.startswith('mince')],
    'Jewelry': [f for f in photos if f.startswith('šperk')]
}

def add_auction_images(auction, category_photos):
    num_images = random.randint(1, 1)  # Počet obrázků
    selected_photos = random.sample(category_photos, num_images)

    for photo in selected_photos:
        photo_path = os.path.join(PHOTO_DIR, photo)

        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo_file:
                auction_image = AuctionImage(auction=auction)
                auction_image.image.save(
                    os.path.join(SAVE_DIR, photo),
                    File(photo_file),
                    save=True
                )


all_users = []

premium_nicks = ["SkylineWalker", "ThunderBlade", "MysticVoyager", "PixelCrafter", "ShadowHunter23", "NeonNinja", "BlazeRunner", "1234"]
user_nicks = ["FrozenPhoenix", "CyberSailor", "EchoJumper", "IronWolfX", "CosmicRider", "LunarKnight7", "SwiftFalcon", "CrimsonEcho"]

for nick in premium_nicks:
    user, created = User.objects.get_or_create(username=nick)
    if created:
        user.set_password('1234')  # Nastavení hesla '1234' pro nového uživatele
        user.save()

        # Nastavení účtu jako 'Premium'
        account_premium, _ = AccountType.objects.get_or_create(account_type='Premium')
        UserAccounts.objects.create(user=user, account_type=account_premium, is_premium=True)

    all_users.append(user)

for nick in user_nicks:
    user, created = User.objects.get_or_create(username=nick)
    if created:
        user.set_password('1234')  # Nastavení hesla '1234' pro nového uživatele
        user.save()
    all_users.append(user)



categories = {
    'Paintings': Category.objects.get_or_create(name='Paintings')[0],
    'Statues': Category.objects.get_or_create(name='Statues')[0],
    'Numismatics': Category.objects.get_or_create(name='Numismatics')[0],
    'Jewelry': Category.objects.get_or_create(name='Jewelry')[0],
}

sample_names = {
    'Paintings': ["Classic Painting", "Sunset Portrait", "Charming Landscape"],
    'Statues': ["Ancient Statue", "Mythical Creature", "Marble Bust"],
    'Numismatics': ["Golden Coin", "Silver Coin Set", "Rare Ancient Coin"],
    'Jewelry': ["Ruby Necklace", "Emerald Ring", "Diamond Earrings"]
}

sample_descriptions = {
    'Paintings': ["A beautiful piece of art from the 18th century.", "An exquisite oil painting with vibrant colors."],
    'Statues': [ "A stunning ancient statue with a rich history.", "A captivating bronze sculpture."],
    'Numismatics': ["Rare coins from the medieval era.", "Silver and gold coins dating back to the Roman Empire."],
    'Jewelry': ["Elegant and unique piece of jewelry, perfect for collectors.", "A dazzling emerald ring set in gold."]
}



def create_expired_auctions_without_bids(
        auction_type,
        users,
        categories,
        sample_names,
        sample_descriptions,
        categorized_photos,
        count=5
):
    for _ in range(count):
        user = random.choice(users)
        category = random.choice(list(categories.values()))
        name_auction = random.choice(sample_names[category.name])
        description = random.choice(sample_descriptions[category.name])

        auction_start_date = timezone.now() - timedelta(days=random.randint(7, 15))
        auction_end_date = auction_start_date + timedelta(days=7)

        add_auction = AddAuction(
            user_creator=user,
            category=category,
            name_auction=name_auction,
            description=description,
            auction_type=auction_type,
            buy_now_price=random.randint(1000, 100000) if auction_type == 'buy_now' else None,
            price=random.randint(1000, 100000) if auction_type == 'place_bid' else None,
            start_price=random.randint(1000, 100000) if auction_type == 'place_bid' else None,
            minimum_bid=random.randint(500, 1000) if auction_type == 'place_bid' else None,
            auction_start_date=auction_start_date,
            auction_end_date=auction_end_date,
            number_of_views=random.randint(0, 500),
            is_sold=False
        )
        add_auction.save()

        add_auction_images(add_auction, categorized_photos[category.name])





















# Vytvoření náhodných příhozů a nastavení kupujícího
def create_random_bids_and_buy_now(auction, users):
    if auction.auction_type == 'place_bid':

        num_bids = random.randint(0, 10)
        current_price = auction.start_price
        previous_price = None

        if num_bids > 0:

            for _ in range(num_bids):
                user = random.choice(users)

                bid_increment = random.randint(auction.minimum_bid, auction.minimum_bid + 1000)
                current_price += bid_increment

                Bid.objects.create(
                    auction=auction,
                    user=user,
                    amount=bid_increment,
                    price=current_price,
                    timestamp=timezone.now()
                )

                auction.name_bider = user
                auction.price = current_price
                auction.previous_price = previous_price
                previous_price = auction.price

            auction.name_buyer = auction.name_bider
            auction.is_sold = True
        else:
            auction.is_sold = False

        auction.auction_end_date = timezone.now()
        auction.save()

    elif auction.auction_type == 'buy_now':

        if random.choice([True, False]):
            user = random.choice(users)
            auction.name_buyer = user
            auction.is_sold = True
            auction.auction_end_date = timezone.now()
        else:
            auction.is_sold = False

        auction.save()


# Vytvoření expirovaných aukcí
def create_expired_auctions_without_bids(
        auction_type,
        users,
        categories,
        sample_names,
        sample_descriptions,
        categorized_photos,
        count=5
):
    for _ in range(count):
        user = random.choice(users)
        category = random.choice(list(categories.values()))
        name_auction = random.choice(sample_names[category.name])
        description = random.choice(sample_descriptions[category.name])

        auction_start_date = timezone.now() - timedelta(days=7)
        auction_end_date = auction_start_date + timedelta(days=7)

        add_auction = AddAuction(
            user_creator=user,
            category=category,
            name_auction=name_auction,
            description=description,
            auction_type=auction_type,
            buy_now_price=random.randint(1000, 100000) if auction_type == 'buy_now' else None,
            price=random.randint(1000, 100000) if auction_type == 'place_bid' else None,
            start_price=random.randint(1000, 100000) if auction_type == 'place_bid' else None,
            minimum_bid=random.randint(500, 1000) if auction_type == 'place_bid' else None,
            auction_start_date=auction_start_date,
            auction_end_date=auction_end_date,
            number_of_views=random.randint(0, 1000),
            is_sold=False
        )
        add_auction.save()

        add_auction_images(add_auction, categorized_photos[category.name])


# Vytvoření aktivních aukcí
def create_active_auctions(
        auction_type,
        users,
        categories,
        sample_names,
        sample_descriptions,
        categorized_photos,
        count=30,
        with_bids=True
):
    for _ in range(count):

        user = random.choice(users)
        category = random.choice(list(categories.values()))
        name_auction = random.choice(sample_names[category.name])
        description = random.choice(sample_descriptions[category.name])

        auction_start_date = timezone.now() - timedelta(days=random.randint(0, 2))
        auction_end_date = timezone.now() + timedelta(days=random.randint(3, 10))

        add_auction = AddAuction(
            user_creator=user,
            category=category,
            name_auction=name_auction,
            description=description,
            auction_type=auction_type,
            buy_now_price=random.randint(1000, 100000) if auction_type == 'buy_now' else None,
            price=random.randint(1000, 100000) if auction_type == 'place_bid' else None,
            start_price=random.randint(1000, 100000) if auction_type == 'place_bid' else None,
            minimum_bid=random.randint(500, 1000) if auction_type == 'place_bid' else None,
            auction_start_date=auction_start_date,
            auction_end_date=auction_end_date,
            number_of_views=random.randint(0, 1000),
            is_sold=False
        )
        add_auction.save()

        add_auction_images(add_auction, categorized_photos[category.name])

        if with_bids and auction_type == 'place_bid':
            create_random_bids_and_buy_now(add_auction, users)


# Hlavní funkce pro spuštění skriptu
def run():









    # Definice kategorizovaných fotografií


    # Vytvoření expirovaných aukcí
    create_expired_auctions_without_bids(
        'buy_now',
        promotion=False,
        users=users,
        categories=categories,
        sample_names=sample_names,
        sample_descriptions=sample_descriptions,
        categorized_photos=categorized_photos,
        count=5
    )

    create_expired_auctions_without_bids(
        'place_bid',
        promotion=True,
        users=users,
        categories=categories,
        sample_names=sample_names,
        sample_descriptions=sample_descriptions,
        categorized_photos=categorized_photos,
        count=5
    )

    create_expired_auctions_without_bids(
        'place_bid',
        promotion=False,
        users=users,
        categories=categories,
        sample_names=sample_names,
        sample_descriptions=sample_descriptions,
        categorized_photos=categorized_photos,
        count=5
    )

    # Vytvoření aktivních aukcí (neexpirovaných)
    create_active_auctions(
        'buy_now',
        promotion=False,
        users=users,
        categories=categories,
        sample_names=sample_names,
        sample_descriptions=sample_descriptions,
        categorized_photos=categorized_photos,
        count=30
    )

    create_active_auctions(
        'place_bid',
        promotion=True,
        users=users,
        categories=categories,
        sample_names=sample_names,
        sample_descriptions=sample_descriptions,
        categorized_photos=categorized_photos,
        count=30,
        with_bids=True
    )

    create_active_auctions(
        'place_bid',
        promotion=False,
        users=users,
        categories=categories,
        sample_names=sample_names,
        sample_descriptions=sample_descriptions,
        categorized_photos=categorized_photos,
        count=30,
        with_bids=True
    )

    print("Data populated successfully!")
