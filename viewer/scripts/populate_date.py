import random
import os
from datetime import timedelta
from django.utils import timezone
from viewer.models import Add_auction, User, Category
from django.core.files import File

# Nastavení cesty k adresáři s fotografiemi
PHOTO_DIR = 'media/photos/'  # Nahraďte touto cestou k vašemu adresáři s fotografiemi
SAVE_DIR = 'photos_add_auction/'  # Složka, kam se budou ukládat nové obrázky

# Seznam souborů fotografií z adresáře
photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif'))]


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

    def random_date_within_a_year():
        start_date = timezone.now() - timedelta(days=365)
        random_days = random.randint(0, 365)
        return start_date + timedelta(days=random_days)

    # Naplňte model Add_auction náhodnými daty
    for _ in range(100):
        user = random.choice(all_users)
        category = random.choice(categories)
        name = random.choice(sample_names[category])
        description = random.choice(sample_descriptions[category])
        minimum_bid = random.randint(50, 500)
        price = random.randint(minimum_bid, minimum_bid + 1000)
        buy_now = random.choice([True, False])
        promotion = random.choice([True, False])
        auction_start_date = random_date_within_a_year()
        auction_end_date = auction_start_date + timedelta(days=random.randint(1, 30))
        number_of_views = random.randint(0, 1000)

        # Náhodně vybere fotku z příslušné kategorie
        if categorized_photos[category]:
            random_photo = random.choice(categorized_photos[category])
            photo_path = os.path.join(PHOTO_DIR, random_photo)

            add_auction = Add_auction(
                user=user,
                category=all_categories[category],
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

            # Přidání fotografie k záznamu Add_auction
            with open(photo_path, 'rb') as photo_file:
                # Ukládání obrázku do nové složky
                add_auction.photo.save(os.path.join(SAVE_DIR, random_photo), File(photo_file), save=True)

            add_auction.save()

    print("Data populated successfully!")






# import random
# import os
# from datetime import timedelta
# from django.utils import timezone
# from viewer.models import Add_auction, User, Category
# from django.core.files import File
#
# # Nastavení cesty k adresáři s fotografiemi
# PHOTO_DIR = 'media/photos/'  # Nahraďte touto cestou k vašemu adresáři s fotografiemi
#
# # Seznam souborů fotografií z adresáře
# photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif'))]
#
#
# # Funkce `run()` jako vstupní bod skriptu
# def run():
#     # Data pro generování záznamů
#     categories = ['Paintings', 'Statues', 'Numismatics', 'Jewelry']
#
#     sample_descriptions = {
#         'Paintings': [
#             "A beautiful piece of art from the 18th century.",
#             "An exquisite oil painting with vibrant colors.",
#             "A charming landscape painting with rich details."
#         ],
#         'Statues': [
#             "A stunning ancient statue with a rich history.",
#             "A finely crafted marble statue from the Renaissance.",
#             "A captivating bronze sculpture."
#         ],
#         'Numismatics': [
#             "Rare coins from the medieval era.",
#             "A collection of ancient coins with historical significance.",
#             "Silver and gold coins dating back to the Roman Empire."
#         ],
#         'Jewelry': [
#             "Elegant and unique piece of jewelry, perfect for collectors.",
#             "A dazzling emerald ring set in gold.",
#             "A delicate diamond necklace with intricate design."
#         ]
#     }
#
#     sample_names = {
#         'Paintings': ["Classic Painting", "Sunset Portrait", "Charming Landscape"],
#         'Statues': ["Ancient Statue", "Mythical Creature", "Marble Bust"],
#         'Numismatics': ["Golden Coin", "Silver Coin Set", "Rare Ancient Coin"],
#         'Jewelry': ["Ruby Necklace", "Emerald Ring", "Diamond Earrings"]
#     }
#
#     # Rozdělení souborů fotografií podle kategorií
#     categorized_photos = {
#         'Paintings': [f for f in photos if f.startswith('obraz')],
#         'Statues': [f for f in photos if f.startswith('socha')],
#         'Numismatics': [f for f in photos if f.startswith('mince')],
#         'Jewelry': [f for f in photos if f.startswith('šperk')]
#     }
#
#     all_categories = {cat: Category.objects.get_or_create(name=cat)[0] for cat in categories}
#     all_users = list(User.objects.all())
#
#     def random_date_within_a_year():
#         start_date = timezone.now() - timedelta(days=365)
#         random_days = random.randint(0, 365)
#         return start_date + timedelta(days=random_days)
#
#     # Naplňte model Add_auction náhodnými daty
#     for _ in range(100):
#         user = random.choice(all_users)
#         category = random.choice(categories)
#         name = random.choice(sample_names[category])
#         description = random.choice(sample_descriptions[category])
#         minimum_bid = random.randint(50, 500)
#         price = random.randint(minimum_bid, minimum_bid + 1000)
#         buy_now = random.choice([True, False])
#         promotion = random.choice([True, False])
#         auction_start_date = random_date_within_a_year()
#         auction_end_date = auction_start_date + timedelta(days=random.randint(1, 30))
#         number_of_views = random.randint(0, 1000)
#
#         # Náhodně vybere fotku z příslušné kategorie
#         if categorized_photos[category]:
#             random_photo = random.choice(categorized_photos[category])
#             photo_path = os.path.join(PHOTO_DIR, random_photo)
#
#             add_auction = Add_auction(
#                 user=user,
#                 category=all_categories[category],
#                 name=name,
#                 description=description,
#                 minimum_bid=minimum_bid,
#                 price=price,
#                 buy_now=buy_now,
#                 promotion=promotion,
#                 auction_start_date=auction_start_date,
#                 auction_end_date=auction_end_date,
#                 number_of_views=number_of_views,
#             )
#
#             # Přidání fotografie k záznamu Add_auction
#             with open(photo_path, 'rb') as photo_file:
#                 add_auction.photo.save(random_photo, File(photo_file), save=True)
#
#             add_auction.save()
#
#     print("Data populated successfully!")






# import random
# import os
# from datetime import timedelta
# from django.utils import timezone
# from viewer.models import Add_auction, User, Category
# from django.core.files import File
#
# # Nastavení cesty k adresáři s fotografiemi
# PHOTO_DIR = 'media/photos/'  # Nahraďte touto cestou k vašemu adresáři s fotografiemi
#
# # Seznam souborů fotografií z adresáře
# photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif'))]
#
# # Funkce `run()` jako vstupní bod skriptu
# def run():
#     # Data pro generování záznamů
#     categories = ['Paintings', 'Statues', 'Numismatics', 'Jewelry']
#     sample_descriptions = {
#         'Paintings': [
#             "A beautiful piece of art from the 18th century.",
#             "An exquisite oil painting with vibrant colors.",
#             "A charming landscape painting with rich details."
#         ],
#         'Statues': [
#             "A stunning ancient statue with a rich history.",
#             "A finely crafted marble statue from the Renaissance.",
#             "A captivating bronze sculpture."
#         ],
#         'Numismatics': [
#             "Rare coins from the medieval era.",
#             "A collection of ancient coins with historical significance.",
#             "Silver and gold coins dating back to the Roman Empire."
#         ],
#         'Jewelry': [
#             "Elegant and unique piece of jewelry, perfect for collectors.",
#             "A dazzling emerald ring set in gold.",
#             "A delicate diamond necklace with intricate design."
#         ]
#     }
#     sample_names = [
#         "Classic Painting", "Ancient Statue", "Golden Coin", "Ruby Necklace",
#         "Sunset Portrait", "Mythical Creature", "Silver Coin Set", "Emerald Ring",
#     ]
#
#     # Rozdělení souborů fotografií podle kategorií
#     categorized_photos = {
#         'Paintings': [f for f in photos if f.startswith('obraz')],
#         'Statues': [f for f in photos if f.startswith('socha')],
#         'Numismatics': [f for f in photos if f.startswith('mince')],
#         'Jewelry': [f for f in photos if f.startswith('šperk')]
#     }
#
#     all_categories = {cat: Category.objects.get_or_create(name=cat)[0] for cat in categories}
#     all_users = list(User.objects.all())
#
#     def random_date_within_a_year():
#         start_date = timezone.now() - timedelta(days=365)
#         random_days = random.randint(0, 365)
#         return start_date + timedelta(days=random_days)
#
#     # Naplňte model Add_auction náhodnými daty
#     for _ in range(100):
#         user = random.choice(all_users)
#         category = random.choice(categories)
#         name = random.choice(sample_names)
#         description = random.choice(sample_descriptions[category])
#         minimum_bid = random.randint(50, 500)
#         price = random.randint(minimum_bid, minimum_bid + 1000)
#         buy_now = random.choice([True, False])
#         promotion = random.choice([True, False])
#         auction_start_date = random_date_within_a_year()
#         auction_end_date = auction_start_date + timedelta(days=random.randint(1, 30))
#         number_of_views = random.randint(0, 1000)
#
#         # Náhodně vybere fotku z příslušné kategorie
#         if categorized_photos[category]:
#             random_photo = random.choice(categorized_photos[category])
#             photo_path = os.path.join(PHOTO_DIR, random_photo)
#
#             add_auction = Add_auction(
#                 user=user,
#                 category=all_categories[category],
#                 name=name,
#                 description=description,
#                 minimum_bid=minimum_bid,
#                 price=price,
#                 buy_now=buy_now,
#                 promotion=promotion,
#                 auction_start_date=auction_start_date,
#                 auction_end_date=auction_end_date,
#                 number_of_views=number_of_views,
#             )
#
#             # Přidání fotografie k záznamu Add_auction
#             with open(photo_path, 'rb') as photo_file:
#                 add_auction.photo.save(random_photo, File(photo_file), save=True)
#
#             add_auction.save()
#
#     print("Data populated successfully!")




# import random
# import os
# from datetime import timedelta
# from django.utils import timezone
# from viewer.models import Add_auction, User, Category
# from django.core.files import File
#
# # Nastavení cesty k adresáři s fotografiemi
# PHOTO_DIR = 'media/photos/'  # Nahraďte touto cestou k vašemu adresáři s fotografiemi
#
# # Seznam souborů fotografií z adresáře
# photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith(('.jpg', '.gif'))]
#
# # Funkce `run()` jako vstupní bod skriptu
# def run():
#     # Data pro generování záznamů
#     categories = ['Paintings', 'Statues', 'Numismatics', 'Jewelry']
#     sample_descriptions = [
#         "A beautiful piece of art from the 18th century.",
#         "A stunning ancient statue with a rich history.",
#         "Rare coins from the medieval era.",
#         "Elegant and unique piece of jewelry, perfect for collectors.",
#         "An exquisite oil painting with vibrant colors.",
#     ]
#     sample_names = [
#         "Classic Painting", "Ancient Statue", "Golden Coin", "Ruby Necklace",
#         "Sunset Portrait", "Mythical Creature", "Silver Coin Set", "Emerald Ring",
#     ]
#
#     all_categories = [Category.objects.get_or_create(name=cat)[0] for cat in categories]
#     all_users = list(User.objects.all())
#
#     def random_date_within_a_year():
#         start_date = timezone.now() - timedelta(days=365)
#         random_days = random.randint(0, 365)
#         return start_date + timedelta(days=random_days)
#
#     # Naplňte model Add_auction náhodnými daty
#     for _ in range(100):
#         user = random.choice(all_users)
#         category = random.choice(all_categories)
#         name = random.choice(sample_names)
#         description = random.choice(sample_descriptions)
#         minimum_bid = random.randint(50, 500)
#         price = random.randint(minimum_bid, minimum_bid + 1000)
#         buy_now = random.choice([True, False])
#         promotion = random.choice([True, False])
#         auction_start_date = random_date_within_a_year()
#         auction_end_date = auction_start_date + timedelta(days=random.randint(1, 30))
#         number_of_views = random.randint(0, 1000)
#
#         # Náhodně vybere fotku z adresáře
#         random_photo = random.choice(photos)
#         photo_path = os.path.join(PHOTO_DIR, random_photo)
#
#         add_auction = Add_auction(
#             user=user,
#             category=category,
#             name=name,
#             description=description,
#             minimum_bid=minimum_bid,
#             price=price,
#             buy_now=buy_now,
#             promotion=promotion,
#             auction_start_date=auction_start_date,
#             auction_end_date=auction_end_date,
#             number_of_views=number_of_views,
#         )
#
#         # Přidání fotografie k záznamu Add_auction
#         with open(photo_path, 'rb') as photo_file:
#             add_auction.photo.save(random_photo, File(photo_file), save=True)
#
#         add_auction.save()
#
#     print("Data populated successfully!")