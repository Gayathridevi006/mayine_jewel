import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings

# ── Shared product catalogue ────────────────────────────────────────────────
PRODUCTS = [
    {"id":1,  "name":"Lakshmi Temple Necklace","category":"gold",   "emoji":"📿","badge":"22K Gold",       "price":128500,"weight":"18g", "purity":"22K",    "description":"A stunning temple necklace inspired by traditional Karnataka craftsmanship. Features intricate Lakshmi motifs with hand-set stones.","in_stock":True},
    {"id":2,  "name":"Bridal Kangan Set",       "category":"bridal","emoji":"💛","badge":"Bridal",         "price":125000,"weight":"45g", "purity":"22K",    "description":"Luxurious bridal kangan set handcrafted in 22K gold. Perfect for weddings and grand occasions.","in_stock":True},
    {"id":3,  "name":"Silver Filigree Jhumkas", "category":"silver","emoji":"✨","badge":"Sterling Silver","price":3200,  "weight":"12g", "purity":"925",    "description":"Delicate handwoven sterling silver jhumkas with fine filigree work. Lightweight and elegant.","in_stock":True},
    {"id":4,  "name":"Gold Mangalsutra",        "category":"gold",  "emoji":"🔮","badge":"22K Gold",       "price":32000, "weight":"10g", "purity":"22K",    "description":"A timeless 22K gold mangalsutra with traditional black bead chain.","in_stock":True},
    {"id":5,  "name":"Custom Name Pendant",     "category":"custom","emoji":"🛠️","badge":"Custom",        "price":8500,  "weight":"4g",  "purity":"18K/22K","description":"Personalised gold pendant with your name or initials. Crafted to order.","in_stock":True},
    {"id":6,  "name":"Silver Anklet Pair",      "category":"silver","emoji":"🌙","badge":"Sterling Silver","price":2800,  "weight":"20g", "purity":"925",    "description":"Traditional 925 sterling silver anklets with ghungroo bells.","in_stock":True},
    {"id":7,  "name":"Bridal Nath",             "category":"bridal","emoji":"💍","badge":"Bridal",         "price":18000, "weight":"6g",  "purity":"22K",    "description":"Ornate bridal nose ring in 22K gold with pearl and stone setting.","in_stock":True},
    {"id":8,  "name":"Gold Kada Bangle",        "category":"gold",  "emoji":"🌀","badge":"22K Gold",       "price":68000, "weight":"25g", "purity":"22K",    "description":"Heavy plain gold kada in 22K. A bold statement piece.","in_stock":False},
    {"id":9,  "name":"Silver Pooja Thali Set",  "category":"silver","emoji":"🪔","badge":"Sterling Silver","price":12500, "weight":"80g", "purity":"999",    "description":"Pure 999 silver pooja thali set with diya, bell, and incense holder.","in_stock":True},
    {"id":10, "name":"Custom Ring Design",      "category":"custom","emoji":"💎","badge":"Custom",         "price":15000, "weight":"5g",  "purity":"18K/22K","description":"Design your own gold ring. Share your idea and our goldsmith brings it to life.","in_stock":True},
    {"id":11, "name":"Bridal Full Set",         "category":"bridal","emoji":"👑","badge":"Bridal",         "price":285000,"weight":"110g","purity":"22K",    "description":"Complete bridal jewellery set — necklace, earrings, bangles, maang tikka, and nath.","in_stock":True},
    {"id":12, "name":"Silver Waist Chain",      "category":"silver","emoji":"⛓️","badge":"Sterling Silver","price":7800,  "weight":"35g", "purity":"925",    "description":"Traditional Karnataka vaddanam-style silver waist chain.","in_stock":True},
]

COLLECTIONS = [
    {"name":"Temple Gold",     "slug":"gold",   "emoji":"📿","count":4, "description":"Timeless temple designs inspired by Karnataka's sacred architecture and Lakshmi iconography.","from_price":"₹32,000"},
    {"name":"Bridal Sets",     "slug":"bridal", "emoji":"👑","count":3, "description":"Curated bridal sets from minimal to grand — each crafted to make your wedding day unforgettable.","from_price":"₹18,000"},
    {"name":"Silver Artistry", "slug":"silver", "emoji":"✨","count":4, "description":"Handcrafted sterling silver pieces from filigree jhumkas to traditional vaddanam.","from_price":"₹2,800"},
    {"name":"Custom Designs",  "slug":"custom", "emoji":"🛠️","count":2, "description":"Completely bespoke jewellery made to your specification. Bring any idea, we craft it.","from_price":"₹5,000"},
    {"name":"Mangalsutras",    "slug":"gold",   "emoji":"🔮","count":3, "description":"Traditional and modern mangalsutras in 22K gold, each with a unique Karnataka craftsmanship.","from_price":"₹28,000"},
    {"name":"Silver Pooja",    "slug":"silver", "emoji":"🪔","count":2, "description":"Sacred silver pooja items — thali sets, diya holders, and incense stands in pure 999 silver.","from_price":"₹8,500"},
]

SHOP_HOURS = [
    {"day":"Monday",    "time":"9:00 AM – 7:00 PM", "closed":False, "today":False},
    {"day":"Tuesday",   "time":"9:00 AM – 7:00 PM", "closed":False, "today":False},
    {"day":"Wednesday", "time":"9:00 AM – 7:00 PM", "closed":False, "today":False},
    {"day":"Thursday",  "time":"9:00 AM – 7:00 PM", "closed":False, "today":False},
    {"day":"Friday",    "time":"9:00 AM – 7:00 PM", "closed":False, "today":False},
    {"day":"Saturday",  "time":"9:00 AM – 6:00 PM", "closed":False, "today":False},
    {"day":"Sunday",    "time":"By Appointment",     "closed":False, "today":False},
]

def _get_product(pid):
    return next((p for p in PRODUCTS if p["id"] == int(pid)), None)

def _mark_today(hours):
    import datetime
    day = datetime.datetime.now().strftime("%A")
    return [{**h, "today": h["day"] == day} for h in hours]


# ── Page views ──────────────────────────────────────────────────────────────

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

def collections(request):
    return render(request, 'mayin/collections.html', {
        'active': 'collections', 'collections': COLLECTIONS,
    })

def bridal(request):
    bridal_products = [p for p in PRODUCTS if p['category'] == 'bridal']
    return render(request, 'mayin/bridal.html', {
        'active': 'bridal', 'bridal_products': bridal_products,
    })

def product_detail(request, product_id):
    product = _get_product(product_id)
    if not product:
        return redirect('home')
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product['id']][:4]
    return render(request, 'mayin/product_detail.html', {
        'active': 'home', 'product': product, 'related': related,
    })

def cart(request):
    return render(request, 'mayin/cart.html', {'active': 'cart'})

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

def about(request):
    return render(request, 'mayin/about.html', {'active': 'about'})

def custom_order(request):
    return render(request, 'mayin/custom_order.html', {
        'active': 'custom_order', 'phone': '+91 9845024348',
        'services': [
            'Custom Gold Necklace Design', 'Bridal Set Creation',
            'Ring Resizing & Redesign', 'Stone Setting & Studding',
            'Antique Jewellery Restoration', 'Name / Initials Pendant',
        ]
    })

def signin(request):
    return render(request, 'mayin/signin.html', {'active': 'signin'})

def signup(request):
    return render(request, 'mayin/signup.html', {})


# ── Metal prices proxy ───────────────────────────────────────────────────────

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
            'gold':   {'price_per_gram':15250.0,'price_per_10g':152500.0,'currency':'INR','change':0,'change_percent':0},
            'silver': {'price_per_gram':250.5,  'price_per_10g':2500.0,  'currency':'INR','change':0,'change_percent':0},
            'last_updated': None, 'source': 'fallback',
            'note': 'Live prices temporarily unavailable.', 'error': str(e)
        })
