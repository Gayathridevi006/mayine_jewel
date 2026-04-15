import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import json
import os
from . import settings # Ensure you have this in your settings.py or .env file
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import json

# ── Product catalogue (replace with DB query in production) ──────────────────
PRODUCTS = [
    {"id": 1,  "name": "Lakshmi Temple Necklace", "category": "gold",   "emoji": "📿", "badge": "22K Gold",        "price": 48500,  "weight": "18g",  "purity": "22K",     "description": "A stunning temple necklace inspired by traditional Karnataka craftsmanship. Features intricate Lakshmi motifs with hand-set stones.", "in_stock": True},
    {"id": 2,  "name": "Bridal Kangan Set",        "category": "bridal", "emoji": "💛", "badge": "Bridal",          "price": 125000, "weight": "45g",  "purity": "22K",     "description": "Luxurious bridal kangan set handcrafted in 22K gold. Perfect for weddings and grand occasions.", "in_stock": True},
    {"id": 3,  "name": "Silver Filigree Jhumkas",  "category": "silver", "emoji": "✨", "badge": "Sterling Silver", "price": 3200,   "weight": "12g",  "purity": "925",     "description": "Delicate handwoven sterling silver jhumkas with fine filigree work. Lightweight and elegant.", "in_stock": True},
    {"id": 4,  "name": "Gold Mangalsutra",         "category": "gold",   "emoji": "🔮", "badge": "22K Gold",        "price": 32000,  "weight": "10g",  "purity": "22K",     "description": "A timeless 22K gold mangalsutra with traditional black bead chain. Symbol of love and commitment.", "in_stock": True},
    {"id": 5,  "name": "Custom Name Pendant",      "category": "custom", "emoji": "🛠️","badge": "Custom",          "price": 8500,   "weight": "4g",   "purity": "18K/22K", "description": "Personalised gold pendant with your name or initials. Crafted to order by our master goldsmith.", "in_stock": True},
    {"id": 6,  "name": "Silver Anklet Pair",       "category": "silver", "emoji": "🌙", "badge": "Sterling Silver", "price": 2800,   "weight": "20g",  "purity": "925",     "description": "Traditional 925 sterling silver anklets with ghungroo bells. Handcrafted with care.", "in_stock": True},
    {"id": 7,  "name": "Bridal Nath",              "category": "bridal", "emoji": "💍", "badge": "Bridal",          "price": 18000,  "weight": "6g",   "purity": "22K",     "description": "Ornate bridal nose ring in 22K gold with pearl and stone setting. A Karnataka wedding essential.", "in_stock": True},
    {"id": 8,  "name": "Gold Kada Bangle",         "category": "gold",   "emoji": "🌀", "badge": "22K Gold",        "price": 68000,  "weight": "25g",  "purity": "22K",     "description": "Heavy plain gold kada in 22K. A bold statement piece that complements both traditional and contemporary wear.", "in_stock": False},
    {"id": 9,  "name": "Silver Pooja Thali Set",   "category": "silver", "emoji": "🪔", "badge": "Sterling Silver", "price": 12500,  "weight": "80g",  "purity": "999",     "description": "Pure 999 silver pooja thali set with diya, bell, and incense holder. Ideal for home rituals.", "in_stock": True},
    {"id": 10, "name": "Custom Ring Design",       "category": "custom", "emoji": "💎", "badge": "Custom",          "price": 15000,  "weight": "5g",   "purity": "18K/22K", "description": "Design your own gold ring. Share your idea and our goldsmith will bring it to life.", "in_stock": True},
    {"id": 11, "name": "Bridal Full Set",          "category": "bridal", "emoji": "👑", "badge": "Bridal",          "price": 285000, "weight": "110g", "purity": "22K",     "description": "Complete bridal jewellery set — necklace, earrings, bangles, maang tikka, and nath. Made to order.", "in_stock": True},
    {"id": 12, "name": "Silver Waist Chain",       "category": "silver", "emoji": "⛓️","badge": "Sterling Silver",  "price": 7800,   "weight": "35g",  "purity": "925",     "description": "Traditional Karnataka vaddanam-style silver waist chain. Handcrafted with oxidised finish.", "in_stock": True},
]


def _get_product(pid):
    return next((p for p in PRODUCTS if p["id"] == int(pid)), None)

def home(request):
    """Main landing page for mayin Jewellery."""
    context = {
        'brand_name': 'mayin',
        'tagline': 'Crafted by a Goldsmith, Worn by Royalty',
        'phone': '+91 9845024348',
        'collections': [
            {
                'name': 'Bridal Gold',
                'description': 'Timeless bridal sets crafted with 22K gold',
                'icon': '💍',
            },
            {
                'name': 'Temple Jewellery',
                'description': 'Sacred designs inspired by Karnataka\'s rich heritage',
                'icon': '🪔',
            },
            {
                'name': 'Silver Filigree',
                'description': 'Delicate handcrafted silver artistry',
                'icon': '✨',
            },
            {
                'name': 'Custom Designs',
                'description': 'Your dream jewellery, brought to life by our master goldsmith',
                'icon': '🛠️',
            },
        ],
        'testimonials': [
            {
                'name': 'Priya S.',
                'location': 'Bengaluru',
                'text': 'My bridal set from mayin was breathtaking. The craftsmanship is unmatched!',
            },
            {
                'name': 'Kavitha R.',
                'location': 'Mysuru',
                'text': 'Ordered a custom necklace and it exceeded all my expectations. Pure artistry.',
            },
            {
                'name': 'Deepa M.',
                'location': 'Mangaluru',
                'text': 'The temple jewellery collection is absolutely divine. Wearing it feels sacred.',
            },
        ],
    }
    return render(request, 'mayin/home.html', context)

def product_detail(request, product_id):
    product = _get_product(product_id)
    if not product:
        return redirect('mayin:home')
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product['id']][:4]
    return render(request, 'mayin/product_detail.html', {'product': product, 'related': related})


def cart(request):
    return render(request, 'mayin/cart.html')


def signin(request):
    return render(request, 'mayin/signin.html')


def signup(request):
    return render(request, 'mayin/signup.html')
def wishlist(request):
    return render(request, 'mayin/wishlist.html', {'active': 'wishlist'})

def orders(request):
    return render(request, 'mayin/orders.html', {'active': 'orders'})

def track_order(request):
    return render(request, 'mayin/track_order.html', {'active': 'track'})

def support(request):
    return render(request, 'mayin/support.html', {
        'active': 'support',
        'hours': _mark_today(SHOP_HOURS),
    })


@require_GET
def get_metal_prices(request):
    """
    API endpoint to fetch live gold and silver prices.
    Uses GoldAPI.io or falls back to a reliable free source.
    Prices returned in INR per gram.
    """
    try:
        # Using metals-api or goldapi — replace API_KEY with your actual key
        # Free alternative: use metals.live or goldpricez scraping
        # For demo, we use goldapi.io free tier

        headers = {
            "x-access-token": settings.API_KEY,
            "Content-Type": "application/json"
        }

        gold_response = requests.get(
            "https://www.goldapi.io/api/XAU/INR",
            headers=headers,
            timeout=5
        )
        silver_response = requests.get(
            "https://www.goldapi.io/api/XAG/INR",
            headers=headers,
            timeout=5
        )

        if gold_response.status_code == 200 and silver_response.status_code == 200:
            gold_data = gold_response.json()
            silver_data = silver_response.json()

            # Convert troy ounce to gram (1 troy oz = 31.1035 g)
            gold_per_gram = round(gold_data.get('price', 0) / 31.1035, 2)
            silver_per_gram = round(silver_data.get('price', 0) / 31.1035, 2)

            return JsonResponse({
                'success': True,
                'gold': {
                    'price_per_gram': gold_per_gram,
                    'price_per_10g': round(gold_per_gram * 10, 2),
                    'currency': 'INR',
                    'change': round(gold_data.get('ch', 0) / 31.1035, 2),
                    'change_percent': round(gold_data.get('chp', 0), 2),
                },
                'silver': {
                    'price_per_gram': silver_per_gram,
                    'price_per_10g': round(silver_per_gram * 10, 2),
                    'currency': 'INR',
                    'change': round(silver_data.get('ch', 0) / 31.1035, 2),
                    'change_percent': round(silver_data.get('chp', 0), 2),
                },
                'last_updated': gold_data.get('timestamp', ''),
                'source': 'goldapi.io'
            })
        else:
            raise Exception("API returned non-200 status")

    except Exception as e:
        # Fallback: return approximate market prices with a note
        # These are example fallback values — update as needed
        return JsonResponse({
            'success': True,
            'gold': {
                'price_per_gram': 7250.00,
                'price_per_10g': 72500.00,
                'currency': 'INR',
                'change': 0,
                'change_percent': 0,
            },
            'silver': {
                'price_per_gram': 88.50,
                'price_per_10g': 885.00,
                'currency': 'INR',
                'change': 0,
                'change_percent': 0,
            },
            'last_updated': None,
            'source': 'fallback',
            'note': 'Live prices temporarily unavailable. Showing approximate values.',
            'error': str(e)
        })


def custom_order(request):
    """Custom order enquiry page."""
    context = {
        'brand_name': 'mayin',
        'phone': '+91 9845024348',
        'services': [
            'Custom Gold Necklace Design',
            'Bridal Set Creation',
            'Ring Resizing & Redesign',
            'Stone Setting & Studding',
            'Antique Jewellery Restoration',
            'Name / Initials Pendant',
        ]
    }
    return render(request, 'mayin/custom_order.html', context)
