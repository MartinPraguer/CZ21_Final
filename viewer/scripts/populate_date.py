import random
import os
from datetime import timedelta
from django.utils import timezone
from viewer.models import Advertisement, User, Category
from django.core.files import File

# Nastavení cesty k adresáři s fotografiemi
PHOTO_DIR = 'media/photos/'  # Nahraďte touto cestou k vašemu adresáři s fotografiemi

# Seznam souborů fotografií z adresáře
photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif'))]

# Funkce `run()` jako vstupní bod skriptu
def run():
    # Data pro generování záznamů
    categories = ['Paintings', 'Statues', 'Numismatics', 'Jewelry']
    sample_descriptions = [
        "A beautiful piece of art from the 18th century.",
        "A stunning ancient statue with a rich history.",
        "Rare coins from the medieval era.",
        "Elegant and unique piece of jewelry, perfect for collectors.",
        "An exquisite oil painting with vibrant colors.",
    ]
    sample_names = [
        "Classic Painting", "Ancient Statue", "Golden Coin", "Ruby Necklace",
        "Sunset Portrait", "Mythical Creature", "Silver Coin Set", "Emerald Ring",
    ]

    all_categories = [Category.objects.get_or_create(name=cat)[0] for cat in categories]
    all_users = list(User.objects.all())

    def random_date_within_a_year():
        start_date = timezone.now() - timedelta(days=365)
        random_days = random.randint(0, 365)
        return start_date + timedelta(days=random_days)

    # Naplňte model Advertisement náhodnými daty
    for _ in range(100):
        user = random.choice(all_users)
        category = random.choice(all_categories)
        name = random.choice(sample_names)
        description = random.choice(sample_descriptions)
        minimum_bid = random.randint(50, 500)
        price = random.randint(minimum_bid, minimum_bid + 1000)
        buy_now = random.choice([True, False])
        promotion = random.choice([True, False])
        auction_start_date = random_date_within_a_year()
        auction_end_date = auction_start_date + timedelta(days=random.randint(1, 30))
        number_of_views = random.randint(0, 1000)

        # Náhodně vybere fotku z adresáře
        random_photo = random.choice(photos)
        photo_path = os.path.join(PHOTO_DIR, random_photo)

        advertisement = Advertisement(
            user=user,
            category=category,
            name=name,
            description=description,
            minimum_bid=minimum_bid,
            price=price,
            buy_now=buy_now,
            promotion=promotion,
            auction_start_date=auction_start_date,
            auction_end_date=auction_end_date,
            number_of_views=number_of_views,
        )

        # Přidání fotografie k záznamu Advertisement
        with open(photo_path, 'rb') as photo_file:
            advertisement.photo.save(random_photo, File(photo_file), save=True)

        advertisement.save()

    print("Data populated successfully!")