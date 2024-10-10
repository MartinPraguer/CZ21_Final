# spuštění - python manage.py runscript populate_date -v3


import random
import os
from datetime import timedelta
from django.utils import timezone
from viewer.models import AddAuction, User, Category
from django.core.files import File

# Nastavení cesty k adresáři s fotografiemi
PHOTO_DIR = 'media/photos/'  # Nahraďte touto cestou k vašemu adresáři s fotografiemi
SAVE_DIR = 'photos_add_auction/'  # Složka, kam se budou ukládat nové obrázky

# Seznam souborů fotografií z adresáře
photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif', '.png'))]

# Funkce pro generování náhodného data začátku a konce aukce
def random_auction_dates():
    # Start aukce od aktuálního času
    auction_start_date = timezone.now()

    # Konec aukce bude náhodně mezi 10 a 15 dny po startu
    random_days = random.randint(10, 15)
    auction_end_date = auction_start_date + timedelta(days=random_days)

    return auction_start_date, auction_end_date

# Funkce `run()` jako vstupní bod skriptu
def run():
    # Data pro generování záznamů
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

    # Rozdělení souborů fotografií podle kategorií
    categorized_photos = {
        'Paintings': [f for f in photos if f.startswith('obraz')],
        'Statues': [f for f in photos if f.startswith('socha')],
        'Numismatics': [f for f in photos if f.startswith('mince')],
        'Jewelry': [f for f in photos if f.startswith('šperk')]
    }

    all_categories = {cat: Category.objects.get_or_create(name=cat)[0] for cat in categories}
    all_users = list(User.objects.all())

    # Naplňte model AddAuction náhodnými daty
    for _ in range(100):
        user = random.choice(all_users)
        category = random.choice(categories)
        name = random.choice(sample_names[category])
        description = random.choice(sample_descriptions[category])
        minimum_bid = random.randint(50, 500)
        buy_now_price = random.randint(minimum_bid + 100, minimum_bid + 1000)
        auction_type = random.choice(['buy_now', 'place_bid'])
        promotion = random.choice([True, False])
        auction_start_date, auction_end_date = random_auction_dates()
        number_of_views = random.randint(0, 1000)

        # Náhodně vybere fotku z příslušné kategorie
        if categorized_photos[category]:
            random_photo = random.choice(categorized_photos[category])
            photo_path = os.path.join(PHOTO_DIR, random_photo)

            add_auction = AddAuction(
                user=user,
                category=all_categories[category],
                name=name,
                description=description,
                minimum_bid=minimum_bid,
                buy_now_price=buy_now_price if auction_type == 'buy_now' else None,
                auction_type=auction_type,
                promotion=promotion,
                auction_start_date=auction_start_date,
                auction_end_date=auction_end_date,
                number_of_views=number_of_views,
            )

            # Přidání fotografie k záznamu AddAuction
            if os.path.exists(photo_path):
                with open(photo_path, 'rb') as photo_file:
                    add_auction.photo.save(os.path.join(SAVE_DIR, random_photo), File(photo_file), save=True)

            add_auction.save()

    print("Data populated successfully!")