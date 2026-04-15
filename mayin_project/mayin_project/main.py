# """
# mayin Jewellery — FastAPI Backend
# Run: uvicorn main:app --reload --port 8001
# Docs: http://localhost:8001/docs
# """

# from fastapi import FastAPI, HTTPException, Depends, status
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional, List
# from datetime import datetime, timedelta
# import uuid, hashlib, hmac, base64, json

# app = FastAPI(title="mayin Jewellery API", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ─────────────────────────────────────────────────────────────────────────────
# # In-memory stores (replace with PostgreSQL / SQLite in production)
# # ─────────────────────────────────────────────────────────────────────────────
# USERS_DB: dict = {}      # email -> user dict
# SESSIONS: dict = {}      # token -> email
# CARTS_DB: dict = {}      # user_id -> list of cart items
# ORDERS_DB: dict = {}     # order_id -> order dict
# WISHLIST_DB: dict = {}   # user_id -> list of product_ids

# SECRET_KEY = "mayin-secret-key-change-in-production"
# security = HTTPBearer(auto_error=False)

# # ─────────────────────────────────────────────────────────────────────────────
# # Product catalogue (mirror of views.py — use a shared DB in production)
# # ─────────────────────────────────────────────────────────────────────────────
# PRODUCTS = [
#     {"id": 1,  "name": "Lakshmi Temple Necklace", "category": "gold",   "emoji": "📿", "badge": "22K Gold",        "price": 48500,  "weight": "18g",  "purity": "22K",     "in_stock": True},
#     {"id": 2,  "name": "Bridal Kangan Set",        "category": "bridal", "emoji": "💛", "badge": "Bridal",          "price": 125000, "weight": "45g",  "purity": "22K",     "in_stock": True},
#     {"id": 3,  "name": "Silver Filigree Jhumkas",  "category": "silver", "emoji": "✨", "badge": "Sterling Silver", "price": 3200,   "weight": "12g",  "purity": "925",     "in_stock": True},
#     {"id": 4,  "name": "Gold Mangalsutra",         "category": "gold",   "emoji": "🔮", "badge": "22K Gold",        "price": 32000,  "weight": "10g",  "purity": "22K",     "in_stock": True},
#     {"id": 5,  "name": "Custom Name Pendant",      "category": "custom", "emoji": "🛠️","badge": "Custom",          "price": 8500,   "weight": "4g",   "purity": "18K/22K", "in_stock": True},
#     {"id": 6,  "name": "Silver Anklet Pair",       "category": "silver", "emoji": "🌙", "badge": "Sterling Silver", "price": 2800,   "weight": "20g",  "purity": "925",     "in_stock": True},
#     {"id": 7,  "name": "Bridal Nath",              "category": "bridal", "emoji": "💍", "badge": "Bridal",          "price": 18000,  "weight": "6g",   "purity": "22K",     "in_stock": True},
#     {"id": 8,  "name": "Gold Kada Bangle",         "category": "gold",   "emoji": "🌀", "badge": "22K Gold",        "price": 68000,  "weight": "25g",  "purity": "22K",     "in_stock": False},
#     {"id": 9,  "name": "Silver Pooja Thali Set",   "category": "silver", "emoji": "🪔", "badge": "Sterling Silver", "price": 12500,  "weight": "80g",  "purity": "999",     "in_stock": True},
#     {"id": 10, "name": "Custom Ring Design",       "category": "custom", "emoji": "💎", "badge": "Custom",          "price": 15000,  "weight": "5g",   "purity": "18K/22K", "in_stock": True},
#     {"id": 11, "name": "Bridal Full Set",          "category": "bridal", "emoji": "👑", "badge": "Bridal",          "price": 285000, "weight": "110g", "purity": "22K",     "in_stock": True},
#     {"id": 12, "name": "Silver Waist Chain",       "category": "silver", "emoji": "⛓️","badge": "Sterling Silver",  "price": 7800,   "weight": "35g",  "purity": "925",     "in_stock": True},
# ]

# # ─────────────────────────────────────────────────────────────────────────────
# # Helpers
# # ─────────────────────────────────────────────────────────────────────────────
# def hash_password(pw: str) -> str:
#     return hashlib.sha256(pw.encode()).hexdigest()

# def make_token(email: str) -> str:
#     token = base64.urlsafe_b64encode(f"{email}:{uuid.uuid4()}".encode()).decode()
#     SESSIONS[token] = email
#     return token

# def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
#     if not creds:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     email = SESSIONS.get(creds.credentials)
#     if not email or email not in USERS_DB:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
#     return USERS_DB[email]

# def optional_user(creds: HTTPAuthorizationCredentials = Depends(security)):
#     if not creds:
#         return None
#     email = SESSIONS.get(creds.credentials)
#     return USERS_DB.get(email)


# # ─────────────────────────────────────────────────────────────────────────────
# # Schemas
# # ─────────────────────────────────────────────────────────────────────────────
# class SignupRequest(BaseModel):
#     first_name: str
#     last_name: str = ""
#     email: EmailStr
#     phone: str = ""
#     city: str = ""
#     password: str = Field(min_length=8)

# class SigninRequest(BaseModel):
#     email: EmailStr
#     password: str

# class CartItem(BaseModel):
#     id: int
#     qty: int = Field(ge=1, le=20)

# class CartUpsertRequest(BaseModel):
#     items: List[CartItem]

# class CheckoutRequest(BaseModel):
#     items: List[dict]
#     address: str = "Karnataka, India"
#     promo_code: str = ""

# class WishlistRequest(BaseModel):
#     product_id: int


# # ─────────────────────────────────────────────────────────────────────────────
# # Auth endpoints
# # ─────────────────────────────────────────────────────────────────────────────
# @app.post("/api/auth/signup", tags=["Auth"])
# def signup(req: SignupRequest):
#     if req.email in USERS_DB:
#         raise HTTPException(status_code=400, detail="Email already registered.")
#     user_id = str(uuid.uuid4())
#     user = {
#         "id": user_id,
#         "first_name": req.first_name,
#         "last_name": req.last_name,
#         "email": req.email,
#         "phone": req.phone,
#         "city": req.city,
#         "password_hash": hash_password(req.password),
#         "created_at": datetime.utcnow().isoformat(),
#     }
#     USERS_DB[req.email] = user
#     CARTS_DB[user_id] = []
#     WISHLIST_DB[user_id] = []
#     token = make_token(req.email)
#     return {
#         "access_token": token,
#         "token_type": "bearer",
#         "user": {k: v for k, v in user.items() if k != "password_hash"}
#     }


# @app.post("/api/auth/signin", tags=["Auth"])
# def signin(req: SigninRequest):
#     user = USERS_DB.get(req.email)
#     if not user or user["password_hash"] != hash_password(req.password):
#         raise HTTPException(status_code=401, detail="Invalid email or password.")
#     token = make_token(req.email)
#     return {
#         "access_token": token,
#         "token_type": "bearer",
#         "user": {k: v for k, v in user.items() if k != "password_hash"}
#     }


# @app.post("/api/auth/signout", tags=["Auth"])
# def signout(creds: HTTPAuthorizationCredentials = Depends(security)):
#     if creds and creds.credentials in SESSIONS:
#         del SESSIONS[creds.credentials]
#     return {"message": "Signed out successfully."}


# @app.get("/api/auth/me", tags=["Auth"])
# def get_me(user=Depends(get_current_user)):
#     return {k: v for k, v in user.items() if k != "password_hash"}


# # ─────────────────────────────────────────────────────────────────────────────
# # Product endpoints
# # ─────────────────────────────────────────────────────────────────────────────
# @app.get("/api/products", tags=["Products"])
# def list_products(category: Optional[str] = None, in_stock: Optional[bool] = None):
#     result = PRODUCTS
#     if category:
#         result = [p for p in result if p["category"] == category]
#     if in_stock is not None:
#         result = [p for p in result if p["in_stock"] == in_stock]
#     return {"products": result, "total": len(result)}


# @app.get("/api/products/{product_id}", tags=["Products"])
# def get_product(product_id: int):
#     product = next((p for p in PRODUCTS if p["id"] == product_id), None)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found.")
#     related = [p for p in PRODUCTS if p["category"] == product["category"] and p["id"] != product_id][:4]
#     return {"product": product, "related": related}


# # ─────────────────────────────────────────────────────────────────────────────
# # Cart endpoints
# # ─────────────────────────────────────────────────────────────────────────────
# @app.get("/api/cart", tags=["Cart"])
# def get_cart(user=Depends(get_current_user)):
#     items = CARTS_DB.get(user["id"], [])
#     enriched = []
#     subtotal = 0
#     for ci in items:
#         p = next((p for p in PRODUCTS if p["id"] == ci["product_id"]), None)
#         if p:
#             line = {**p, "qty": ci["qty"], "subtotal": p["price"] * ci["qty"]}
#             enriched.append(line)
#             subtotal += line["subtotal"]
#     shipping = 0 if subtotal >= 50000 else 299
#     gst = round(subtotal * 0.03)
#     return {
#         "items": enriched,
#         "subtotal": subtotal,
#         "shipping": shipping,
#         "gst": gst,
#         "total": subtotal + shipping + gst,
#         "item_count": sum(i["qty"] for i in items),
#     }


# @app.post("/api/cart/add", tags=["Cart"])
# def add_to_cart(item: CartItem, user=Depends(get_current_user)):
#     product = next((p for p in PRODUCTS if p["id"] == item.id), None)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found.")
#     if not product["in_stock"]:
#         raise HTTPException(status_code=400, detail="Product is out of stock.")
#     cart = CARTS_DB.get(user["id"], [])
#     idx = next((i for i, c in enumerate(cart) if c["product_id"] == item.id), None)
#     if idx is not None:
#         cart[idx]["qty"] = min(20, cart[idx]["qty"] + item.qty)
#     else:
#         cart.append({"product_id": item.id, "qty": item.qty})
#     CARTS_DB[user["id"]] = cart
#     return {"message": "Added to cart.", "cart_count": sum(c["qty"] for c in cart)}


# @app.put("/api/cart/update", tags=["Cart"])
# def update_cart(req: CartUpsertRequest, user=Depends(get_current_user)):
#     cart = [{"product_id": i.id, "qty": i.qty} for i in req.items if i.qty > 0]
#     CARTS_DB[user["id"]] = cart
#     return {"message": "Cart updated.", "cart_count": sum(c["qty"] for c in cart)}


# @app.delete("/api/cart/{product_id}", tags=["Cart"])
# def remove_from_cart(product_id: int, user=Depends(get_current_user)):
#     cart = [c for c in CARTS_DB.get(user["id"], []) if c["product_id"] != product_id]
#     CARTS_DB[user["id"]] = cart
#     return {"message": "Item removed.", "cart_count": sum(c["qty"] for c in cart)}


# @app.delete("/api/cart", tags=["Cart"])
# def clear_cart(user=Depends(get_current_user)):
#     CARTS_DB[user["id"]] = []
#     return {"message": "Cart cleared."}


# # ─────────────────────────────────────────────────────────────────────────────
# # Orders endpoint
# # ─────────────────────────────────────────────────────────────────────────────
# @app.post("/api/orders/checkout", tags=["Orders"])
# def checkout(req: CheckoutRequest, user=Depends(get_current_user)):
#     if not req.items:
#         raise HTTPException(status_code=400, detail="Cart is empty.")
#     order_id = "MJO-" + str(uuid.uuid4())[:8].upper()
#     subtotal = sum(i.get("price", 0) * i.get("qty", 1) for i in req.items)
#     shipping = 0 if subtotal >= 50000 else 299
#     gst = round(subtotal * 0.03)
#     order = {
#         "order_id": order_id,
#         "user_id": user["id"],
#         "user_email": user["email"],
#         "items": req.items,
#         "address": req.address,
#         "subtotal": subtotal,
#         "shipping": shipping,
#         "gst": gst,
#         "total": subtotal + shipping + gst,
#         "status": "confirmed",
#         "created_at": datetime.utcnow().isoformat(),
#     }
#     ORDERS_DB[order_id] = order
#     CARTS_DB[user["id"]] = []
#     return {
#         "order_id": order_id,
#         "total": order["total"],
#         "status": "confirmed",
#         "message": f"Order {order_id} placed successfully! We will contact you at {user.get('phone','your number')} for delivery.",
#     }


# @app.get("/api/orders", tags=["Orders"])
# def get_orders(user=Depends(get_current_user)):
#     orders = [o for o in ORDERS_DB.values() if o["user_id"] == user["id"]]
#     return {"orders": sorted(orders, key=lambda o: o["created_at"], reverse=True)}


# @app.get("/api/orders/{order_id}", tags=["Orders"])
# def get_order(order_id: str, user=Depends(get_current_user)):
#     order = ORDERS_DB.get(order_id)
#     if not order or order["user_id"] != user["id"]:
#         raise HTTPException(status_code=404, detail="Order not found.")
#     return order


# # ─────────────────────────────────────────────────────────────────────────────
# # Wishlist endpoints
# # ─────────────────────────────────────────────────────────────────────────────
# @app.get("/api/wishlist", tags=["Wishlist"])
# def get_wishlist(user=Depends(get_current_user)):
#     ids = WISHLIST_DB.get(user["id"], [])
#     products = [p for p in PRODUCTS if p["id"] in ids]
#     return {"wishlist": products}


# @app.post("/api/wishlist", tags=["Wishlist"])
# def toggle_wishlist(req: WishlistRequest, user=Depends(get_current_user)):
#     ids = WISHLIST_DB.get(user["id"], [])
#     if req.product_id in ids:
#         ids.remove(req.product_id)
#         action = "removed"
#     else:
#         ids.append(req.product_id)
#         action = "added"
#     WISHLIST_DB[user["id"]] = ids
#     return {"action": action, "product_id": req.product_id, "wishlist_count": len(ids)}


# # ─────────────────────────────────────────────────────────────────────────────
# # Metal prices proxy
# # ─────────────────────────────────────────────────────────────────────────────
# @app.get("/api/metal-prices", tags=["Prices"])
# def metal_prices():
#     import httpx
#     try:
#         API_KEY = "YOUR_GOLDAPI_KEY"
#         headers = {"x-access-token": API_KEY, "Content-Type": "application/json"}
#         with httpx.Client(timeout=5) as client:
#             gr = client.get("https://www.goldapi.io/api/XAU/INR", headers=headers)
#             sr = client.get("https://www.goldapi.io/api/XAG/INR", headers=headers)
#         if gr.status_code == 200 and sr.status_code == 200:
#             gd, sd = gr.json(), sr.json()
#             gpg = round(gd.get("price", 0) / 31.1035, 2)
#             spg = round(sd.get("price", 0) / 31.1035, 2)
#             return {
#                 "success": True,
#                 "gold":   {"price_per_gram": gpg, "price_per_10g": round(gpg*10, 2), "currency": "INR", "change": round(gd.get("ch",0)/31.1035,2), "change_percent": round(gd.get("chp",0),2)},
#                 "silver": {"price_per_gram": spg, "price_per_10g": round(spg*10, 2), "currency": "INR", "change": round(sd.get("ch",0)/31.1035,2), "change_percent": round(sd.get("chp",0),2)},
#                 "last_updated": gd.get("timestamp"), "source": "goldapi.io"
#             }
#     except Exception as e:
#         pass
#     return {
#         "success": True,
#         "gold":   {"price_per_gram": 7250.0, "price_per_10g": 72500.0, "currency": "INR", "change": 0, "change_percent": 0},
#         "silver": {"price_per_gram": 88.5,   "price_per_10g": 885.0,   "currency": "INR", "change": 0, "change_percent": 0},
#         "last_updated": None, "source": "fallback", "note": "Live prices temporarily unavailable."
#     }


# # ─────────────────────────────────────────────────────────────────────────────
# # Health check
# # ─────────────────────────────────────────────────────────────────────────────
# @app.get("/api/health", tags=["System"])
# def health():
#     return {"status": "ok", "service": "mayin Jewellery API", "version": "1.0.0"}
"""
mayin Jewellery — FastAPI Backend
Run: uvicorn main:app --reload --port 8001
Docs: http://localhost:8001/docs
"""
import httpx
from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import uuid, hashlib, base64

app = FastAPI(title="Mayin Jewellery API", version="2.0.0", description="Backend for Mayin Jewellery — Karnataka's handcrafted gold & silver")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)

# ─────────────────────────────────────────────────────────────
# IN-MEMORY STORES  (swap for PostgreSQL in production)
# ─────────────────────────────────────────────────────────────
USERS:     dict = {}   # email → user
SESSIONS:  dict = {}   # token → email
CARTS:     dict = {}   # user_id → [{product_id, qty}]
ORDERS:    dict = {}   # order_id → order
WISHLISTS: dict = {}   # user_id → [product_ids]
REVIEWS:   dict = {}   # product_id → [review]
TICKETS:   dict = {}   # ticket_id → ticket
ADDRESSES: dict = {}   # user_id → [address]

# ─────────────────────────────────────────────────────────────
# PRODUCT CATALOGUE
# ─────────────────────────────────────────────────────────────
PRODUCTS = [
    {"id":1,  "name":"Lakshmi Temple Necklace","category":"gold",   "emoji":"📿","badge":"22K Gold",       "price":128500,"weight":"18g","purity":"22K",    "in_stock":True, "rating":4.9,"review_count":34},
    {"id":2,  "name":"Bridal Kangan Set",       "category":"bridal","emoji":"💛","badge":"Bridal",         "price":125000,"weight":"45g","purity":"22K",    "in_stock":True, "rating":5.0,"review_count":18},
    {"id":3,  "name":"Silver Filigree Jhumkas", "category":"silver","emoji":"✨","badge":"Sterling Silver","price":3200,  "weight":"12g","purity":"925",    "in_stock":True, "rating":4.8,"review_count":52},
    {"id":4,  "name":"Gold Mangalsutra",        "category":"gold",  "emoji":"🔮","badge":"22K Gold",       "price":32000, "weight":"10g","purity":"22K",    "in_stock":True, "rating":4.7,"review_count":29},
    {"id":5,  "name":"Custom Name Pendant",     "category":"custom","emoji":"🛠️","badge":"Custom",        "price":8500,  "weight":"4g", "purity":"18K/22K","in_stock":True, "rating":5.0,"review_count":41},
    {"id":6,  "name":"Silver Anklet Pair",      "category":"silver","emoji":"🌙","badge":"Sterling Silver","price":2800,  "weight":"20g","purity":"925",    "in_stock":True, "rating":4.6,"review_count":67},
    {"id":7,  "name":"Bridal Nath",             "category":"bridal","emoji":"💍","badge":"Bridal",         "price":18000, "weight":"6g", "purity":"22K",    "in_stock":True, "rating":4.9,"review_count":22},
    {"id":8,  "name":"Gold Kada Bangle",        "category":"gold",  "emoji":"🌀","badge":"22K Gold",       "price":68000, "weight":"25g","purity":"22K",    "in_stock":False,"rating":4.8,"review_count":15},
    {"id":9,  "name":"Silver Pooja Thali Set",  "category":"silver","emoji":"🪔","badge":"Sterling Silver","price":12500, "weight":"80g","purity":"999",    "in_stock":True, "rating":4.7,"review_count":38},
    {"id":10, "name":"Custom Ring Design",      "category":"custom","emoji":"💎","badge":"Custom",         "price":15000, "weight":"5g", "purity":"18K/22K","in_stock":True, "rating":5.0,"review_count":27},
    {"id":11, "name":"Bridal Full Set",         "category":"bridal","emoji":"👑","badge":"Bridal",         "price":285000,"weight":"110g","purity":"22K",   "in_stock":True, "rating":5.0,"review_count":9},
    {"id":12, "name":"Silver Waist Chain",      "category":"silver","emoji":"⛓️","badge":"Sterling Silver","price":7800,  "weight":"35g","purity":"925",    "in_stock":True, "rating":4.5,"review_count":43},
]

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def make_token(email):
    t = base64.urlsafe_b64encode(f"{email}:{uuid.uuid4()}".encode()).decode()
    SESSIONS[t] = email; return t
def get_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not creds: raise HTTPException(401, "Not authenticated")
    email = SESSIONS.get(creds.credentials)
    if not email or email not in USERS: raise HTTPException(401, "Invalid or expired token")
    return USERS[email]
def opt_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not creds: return None
    return USERS.get(SESSIONS.get(creds.credentials))
def find_product(pid): return next((p for p in PRODUCTS if p["id"] == pid), None)
def now_iso(): return datetime.utcnow().isoformat()

# ─────────────────────────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────────────────────────
class SignupReq(BaseModel):
    first_name: str; last_name: str = ""; email: EmailStr
    phone: str = ""; city: str = ""; password: str = Field(min_length=8)

class SigninReq(BaseModel):
    email: EmailStr; password: str

class CartItem(BaseModel):
    id: int; qty: int = Field(ge=1, le=20)

class CartSyncReq(BaseModel):
    items: List[CartItem]

class CheckoutReq(BaseModel):
    items: List[dict]; address: str = "Karnataka, India"; promo_code: str = ""

class ReviewReq(BaseModel):
    rating: int = Field(ge=1, le=5); comment: str; name: str = ""

class SupportTicketReq(BaseModel):
    name: str; contact: str; topic: str = "other"; message: str

class CustomOrderReq(BaseModel):
    name: str; phone: str; city: str = ""; metal: str = "22K Gold"
    jewellery_type: str = ""; budget: str = ""; description: str

class AddressReq(BaseModel):
    label: str = "Home"; line1: str; line2: str = ""; city: str
    state: str = "Karnataka"; pincode: str; phone: str

class WishlistReq(BaseModel):
    product_id: int


# ─────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────
@app.post("/api/auth/signup", tags=["Auth"], summary="Register a new account")
def signup(req: SignupReq):
    if req.email in USERS:
        raise HTTPException(400, "Email already registered.")
    uid = str(uuid.uuid4())
    user = {"id": uid, "first_name": req.first_name, "last_name": req.last_name,
            "email": req.email, "phone": req.phone, "city": req.city,
            "password_hash": hash_pw(req.password), "created_at": now_iso()}
    USERS[req.email] = user
    CARTS[uid] = []; WISHLISTS[uid] = []; ADDRESSES[uid] = []
    token = make_token(req.email)
    return {"access_token": token, "token_type": "bearer",
            "user": {k:v for k,v in user.items() if k != "password_hash"}}

@app.post("/api/auth/signin", tags=["Auth"], summary="Sign in")
def signin(req: SigninReq):
    user = USERS.get(req.email)
    if not user or user["password_hash"] != hash_pw(req.password):
        raise HTTPException(401, "Invalid email or password.")
    token = make_token(req.email)
    return {"access_token": token, "token_type": "bearer",
            "user": {k:v for k,v in user.items() if k != "password_hash"}}

@app.post("/api/auth/signout", tags=["Auth"])
def signout(creds: HTTPAuthorizationCredentials = Depends(security)):
    if creds and creds.credentials in SESSIONS: del SESSIONS[creds.credentials]
    return {"message": "Signed out."}

@app.get("/api/auth/me", tags=["Auth"])
def me(user=Depends(get_user)):
    return {k:v for k,v in user.items() if k != "password_hash"}

@app.put("/api/auth/me", tags=["Auth"], summary="Update profile")
def update_me(data: dict, user=Depends(get_user)):
    allowed = {"first_name","last_name","phone","city"}
    for k,v in data.items():
        if k in allowed: user[k] = v
    return {k:v for k,v in user.items() if k != "password_hash"}


# ─────────────────────────────────────────────────────────────
# PRODUCTS
# ─────────────────────────────────────────────────────────────
@app.get("/api/products", tags=["Products"], summary="List all products")
def list_products(
    category: Optional[str] = None,
    in_stock: Optional[bool] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    sort: Optional[str] = Query(None, enum=["price_asc","price_desc","rating","newest"]),
):
    result = list(PRODUCTS)
    if category:  result = [p for p in result if p["category"] == category]
    if in_stock is not None: result = [p for p in result if p["in_stock"] == in_stock]
    if min_price: result = [p for p in result if p["price"] >= min_price]
    if max_price: result = [p for p in result if p["price"] <= max_price]
    if sort == "price_asc":  result.sort(key=lambda p: p["price"])
    if sort == "price_desc": result.sort(key=lambda p: p["price"], reverse=True)
    if sort == "rating":     result.sort(key=lambda p: p["rating"], reverse=True)
    return {"products": result, "total": len(result)}

@app.get("/api/products/{product_id}", tags=["Products"])
def get_product(product_id: int):
    p = find_product(product_id)
    if not p: raise HTTPException(404, "Product not found.")
    related = [x for x in PRODUCTS if x["category"] == p["category"] and x["id"] != product_id][:4]
    revs = REVIEWS.get(product_id, [])
    return {"product": p, "related": related, "reviews": revs[-10:], "review_count": len(revs)}

@app.get("/api/products/search/{query}", tags=["Products"])
def search_products(query: str):
    q = query.lower()
    result = [p for p in PRODUCTS if q in p["name"].lower() or q in p["category"].lower() or q in p["badge"].lower()]
    return {"products": result, "total": len(result), "query": query}


# ─────────────────────────────────────────────────────────────
# REVIEWS
# ─────────────────────────────────────────────────────────────
@app.get("/api/products/{product_id}/reviews", tags=["Reviews"])
def get_reviews(product_id: int):
    p = find_product(product_id)
    if not p: raise HTTPException(404, "Product not found.")
    return {"reviews": REVIEWS.get(product_id, []), "product_id": product_id}

@app.post("/api/products/{product_id}/reviews", tags=["Reviews"])
def add_review(product_id: int, req: ReviewReq, user=Depends(get_user)):
    p = find_product(product_id)
    if not p: raise HTTPException(404, "Product not found.")
    rev = {"id": str(uuid.uuid4()), "user_id": user["id"],
           "name": req.name or user["first_name"],
           "rating": req.rating, "comment": req.comment, "created_at": now_iso()}
    if product_id not in REVIEWS: REVIEWS[product_id] = []
    REVIEWS[product_id].append(rev)
    # Update product rating average
    revs = REVIEWS[product_id]
    avg = round(sum(r["rating"] for r in revs) / len(revs), 1)
    for prod in PRODUCTS:
        if prod["id"] == product_id:
            prod["rating"] = avg; prod["review_count"] = len(revs)
    return {"review": rev, "new_rating": avg}


# ─────────────────────────────────────────────────────────────
# CART
# ─────────────────────────────────────────────────────────────
def _build_cart(user_id):
    items = CARTS.get(user_id, [])
    enriched = []
    subtotal = 0
    for ci in items:
        p = find_product(ci["product_id"])
        if p:
            sub = p["price"] * ci["qty"]
            enriched.append({**p, "qty": ci["qty"], "subtotal": sub})
            subtotal += sub
    shipping = 0 if subtotal >= 50000 else 299
    gst = round(subtotal * 0.03)
    return {"items": enriched, "subtotal": subtotal, "shipping": shipping,
            "gst": gst, "total": subtotal + shipping + gst,
            "item_count": sum(i["qty"] for i in items)}

@app.get("/api/cart", tags=["Cart"])
def get_cart(user=Depends(get_user)):
    return _build_cart(user["id"])

@app.post("/api/cart/add", tags=["Cart"])
def add_to_cart(item: CartItem, user=Depends(get_user)):
    p = find_product(item.id)
    if not p: raise HTTPException(404, "Product not found.")
    if not p["in_stock"]: raise HTTPException(400, "Product out of stock.")
    cart = CARTS.get(user["id"], [])
    idx = next((i for i,c in enumerate(cart) if c["product_id"] == item.id), None)
    if idx is not None: cart[idx]["qty"] = min(20, cart[idx]["qty"] + item.qty)
    else: cart.append({"product_id": item.id, "qty": item.qty})
    CARTS[user["id"]] = cart
    return {"message": "Added.", "cart_count": sum(c["qty"] for c in cart)}

@app.put("/api/cart/sync", tags=["Cart"], summary="Sync full cart (from localStorage)")
def sync_cart(req: CartSyncReq, user=Depends(get_user)):
    CARTS[user["id"]] = [{"product_id": i.id, "qty": i.qty} for i in req.items if i.qty > 0]
    return _build_cart(user["id"])

@app.delete("/api/cart/{product_id}", tags=["Cart"])
def remove_from_cart(product_id: int, user=Depends(get_user)):
    CARTS[user["id"]] = [c for c in CARTS.get(user["id"],[]) if c["product_id"] != product_id]
    return {"message": "Removed.", "cart": _build_cart(user["id"])}

@app.delete("/api/cart", tags=["Cart"])
def clear_cart(user=Depends(get_user)):
    CARTS[user["id"]] = []; return {"message": "Cart cleared."}


# ─────────────────────────────────────────────────────────────
# ORDERS
# ─────────────────────────────────────────────────────────────
@app.post("/api/orders/checkout", tags=["Orders"])
def checkout(req: CheckoutReq, user=Depends(get_user)):
    if not req.items: raise HTTPException(400, "Cart is empty.")
    discount = 0
    if req.promo_code.upper() == "MAYIN10": discount = 10
    oid = "MJO-" + str(uuid.uuid4())[:8].upper()
    subtotal = sum(i.get("price",0) * i.get("qty",1) for i in req.items)
    shipping = 0 if subtotal >= 50000 else 299
    gst = round(subtotal * 0.03)
    disc_amt = round(subtotal * discount / 100)
    total = subtotal + shipping + gst - disc_amt
    order = {"order_id": oid, "user_id": user["id"], "user_email": user["email"],
             "items": req.items, "address": req.address, "subtotal": subtotal,
             "shipping": shipping, "gst": gst, "discount": disc_amt, "total": total,
             "status": "confirmed", "created_at": now_iso(), "promo": req.promo_code}
    ORDERS[oid] = order
    CARTS[user["id"]] = []
    return {"order_id": oid, "total": total, "status": "confirmed",
            "message": f"Order {oid} confirmed! We'll call {user.get('phone','you')} shortly."}

@app.get("/api/orders", tags=["Orders"])
def list_orders(user=Depends(get_user)):
    orders = sorted([o for o in ORDERS.values() if o["user_id"] == user["id"]],
                    key=lambda o: o["created_at"], reverse=True)
    return {"orders": orders, "total": len(orders)}

@app.get("/api/orders/{order_id}", tags=["Orders"])
def get_order(order_id: str, user: Optional[dict] = Depends(opt_user)):
    order = ORDERS.get(order_id.upper())
    if not order: raise HTTPException(404, "Order not found.")
    if user and order["user_id"] != user["id"]: raise HTTPException(403, "Access denied.")
    return order

@app.put("/api/orders/{order_id}/status", tags=["Orders"], summary="Update order status (admin)")
def update_order_status(order_id: str, status: str):
    valid = ["confirmed","processing","quality","shipped","delivered","cancelled"]
    if status not in valid: raise HTTPException(400, f"Invalid status. Use one of: {valid}")
    order = ORDERS.get(order_id.upper())
    if not order: raise HTTPException(404, "Order not found.")
    order["status"] = status; order["updated_at"] = now_iso()
    return {"order_id": order_id, "status": status}


# ─────────────────────────────────────────────────────────────
# WISHLIST
# ─────────────────────────────────────────────────────────────
@app.get("/api/wishlist", tags=["Wishlist"])
def get_wishlist(user=Depends(get_user)):
    ids = WISHLISTS.get(user["id"], [])
    return {"wishlist": [p for p in PRODUCTS if p["id"] in ids], "count": len(ids)}

@app.post("/api/wishlist/toggle", tags=["Wishlist"])
def toggle_wishlist(req: WishlistReq, user=Depends(get_user)):
    ids = WISHLISTS.get(user["id"], [])
    if req.product_id in ids: ids.remove(req.product_id); action = "removed"
    else: ids.append(req.product_id); action = "added"
    WISHLISTS[user["id"]] = ids
    return {"action": action, "product_id": req.product_id, "count": len(ids)}

@app.delete("/api/wishlist/{product_id}", tags=["Wishlist"])
def remove_wishlist(product_id: int, user=Depends(get_user)):
    ids = [x for x in WISHLISTS.get(user["id"],[]) if x != product_id]
    WISHLISTS[user["id"]] = ids
    return {"message": "Removed.", "count": len(ids)}


# ─────────────────────────────────────────────────────────────
# ADDRESSES
# ─────────────────────────────────────────────────────────────
@app.get("/api/addresses", tags=["Addresses"])
def get_addresses(user=Depends(get_user)):
    return {"addresses": ADDRESSES.get(user["id"], [])}

@app.post("/api/addresses", tags=["Addresses"])
def add_address(req: AddressReq, user=Depends(get_user)):
    addr = {"id": str(uuid.uuid4()), **req.dict(), "created_at": now_iso()}
    addrs = ADDRESSES.get(user["id"], [])
    addrs.append(addr)
    ADDRESSES[user["id"]] = addrs
    return {"address": addr, "total": len(addrs)}

@app.delete("/api/addresses/{address_id}", tags=["Addresses"])
def delete_address(address_id: str, user=Depends(get_user)):
    addrs = [a for a in ADDRESSES.get(user["id"],[]) if a["id"] != address_id]
    ADDRESSES[user["id"]] = addrs
    return {"message": "Deleted.", "total": len(addrs)}


# ─────────────────────────────────────────────────────────────
# SUPPORT TICKETS
# ─────────────────────────────────────────────────────────────
@app.post("/api/support/ticket", tags=["Support"], summary="Submit a support ticket")
def submit_ticket(req: SupportTicketReq):
    tid = "TKT-" + str(uuid.uuid4())[:6].upper()
    ticket = {"ticket_id": tid, "name": req.name, "contact": req.contact,
              "topic": req.topic, "message": req.message,
              "status": "open", "created_at": now_iso()}
    TICKETS[tid] = ticket
    return {"ticket_id": tid, "status": "open",
            "message": f"Ticket {tid} received. We'll contact you at {req.contact} within 24 hours."}

@app.get("/api/support/ticket/{ticket_id}", tags=["Support"])
def get_ticket(ticket_id: str):
    t = TICKETS.get(ticket_id.upper())
    if not t: raise HTTPException(404, "Ticket not found.")
    return t

@app.get("/api/support/tickets", tags=["Support"], summary="List all tickets (admin)")
def list_tickets():
    return {"tickets": list(TICKETS.values()), "total": len(TICKETS)}


# ─────────────────────────────────────────────────────────────
# CUSTOM ORDERS
# ─────────────────────────────────────────────────────────────
@app.post("/api/custom-orders", tags=["Custom Orders"], summary="Submit a custom design request")
def submit_custom_order(req: CustomOrderReq):
    cid = "CUS-" + str(uuid.uuid4())[:8].upper()
    order = {"custom_order_id": cid, **req.dict(), "status": "received", "created_at": now_iso()}
    ORDERS["custom_" + cid] = order
    return {"custom_order_id": cid, "status": "received",
            "message": f"Custom order {cid} received! Our goldsmith will call {req.phone} within 24 hours."}

@app.get("/api/custom-orders", tags=["Custom Orders"])
def list_custom_orders():
    orders = [o for k,o in ORDERS.items() if k.startswith("custom_")]
    return {"orders": orders, "total": len(orders)}


# ─────────────────────────────────────────────────────────────
# COLLECTIONS
# ─────────────────────────────────────────────────────────────
@app.get("/api/collections", tags=["Collections"])
def get_collections():
    cats = {}
    for p in PRODUCTS:
        c = p["category"]
        if c not in cats: cats[c] = {"category": c, "count": 0, "min_price": p["price"], "max_price": p["price"], "products": []}
        cats[c]["count"] += 1
        cats[c]["min_price"] = min(cats[c]["min_price"], p["price"])
        cats[c]["max_price"] = max(cats[c]["max_price"], p["price"])
        cats[c]["products"].append(p["id"])
    return {"collections": list(cats.values())}


# ─────────────────────────────────────────────────────────────
# METAL PRICES
# ─────────────────────────────────────────────────────────────
@app.get("/api/metal-prices", tags=["Prices"])
def metal_prices():
    try:
        import httpx
        with httpx.Client(timeout=5) as client:
            API_KEY = "YOUR_GOLDAPI_KEY"
            h = {"x-access-token": API_KEY, "Content-Type": "application/json"}
            gr = client.get("https://www.goldapi.io/api/XAU/INR", headers=h)
            sr = client.get("https://www.goldapi.io/api/XAG/INR", headers=h)
        if gr.status_code == 200 and sr.status_code == 200:
            gd, sd = gr.json(), sr.json()
            gpg = round(gd.get("price",0)/31.1035, 2)
            spg = round(sd.get("price",0)/31.1035, 2)
            return {"success":True,
                    "gold":  {"price_per_gram":gpg,"price_per_10g":round(gpg*10,2),"currency":"INR","change":round(gd.get("ch",0)/31.1035,2),"change_percent":round(gd.get("chp",0),2)},
                    "silver":{"price_per_gram":spg,"price_per_10g":round(spg*10,2),"currency":"INR","change":round(sd.get("ch",0)/31.1035,2),"change_percent":round(sd.get("chp",0),2)},
                    "last_updated":gd.get("timestamp"),"source":"goldapi.io"}
    except: pass
    return {"success":True,
            "gold":  {"price_per_gram":7250.0,"price_per_10g":72500.0,"currency":"INR","change":0,"change_percent":0},
            "silver":{"price_per_gram":88.5,  "price_per_10g":885.0,  "currency":"INR","change":0,"change_percent":0},
            "last_updated":None,"source":"fallback","note":"Live prices temporarily unavailable."}


# ─────────────────────────────────────────────────────────────
# PROMO CODES
# ─────────────────────────────────────────────────────────────
PROMO_CODES = {
    "MAYIN10":   {"discount_pct": 10, "description": "10% off your order", "active": True},
    "BRIDAL15":  {"discount_pct": 15, "description": "15% off bridal sets", "active": True},
    "FIRST5":    {"discount_pct":  5, "description": "5% off first order",  "active": True},
}

@app.get("/api/promo/{code}", tags=["Promo"])
def validate_promo(code: str):
    p = PROMO_CODES.get(code.upper())
    if not p or not p["active"]: raise HTTPException(404, "Invalid or expired promo code.")
    return {"code": code.upper(), "discount_percent": p["discount_pct"], "description": p["description"]}


# ─────────────────────────────────────────────────────────────
# HEALTH
# ─────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["System"])
def health():
    return {"status":"ok","service":"Mayin Jewellery API","version":"2.0.0",
            "users":len(USERS),"orders":len(ORDERS),"tickets":len(TICKETS)}

# ─────────────────────────────────────────────────────────────────────────────
# In-memory stores (replace with PostgreSQL / SQLite in production)
# ─────────────────────────────────────────────────────────────────────────────
USERS_DB: dict = {}      # email -> user dict
SESSIONS: dict = {}      # token -> email
CARTS_DB: dict = {}      # user_id -> list of cart items
ORDERS_DB: dict = {}     # order_id -> order dict
WISHLIST_DB: dict = {}   # user_id -> list of product_ids

SECRET_KEY = "mayin-secret-key-change-in-production"
security = HTTPBearer(auto_error=False)

# ─────────────────────────────────────────────────────────────────────────────
# Product catalogue (mirror of views.py — use a shared DB in production)
# ─────────────────────────────────────────────────────────────────────────────
PRODUCTS = [
    {"id": 1,  "name": "Lakshmi Temple Necklace", "category": "gold",   "emoji": "📿", "badge": "22K Gold",        "price": 48500,  "weight": "18g",  "purity": "22K",     "in_stock": True},
    {"id": 2,  "name": "Bridal Kangan Set",        "category": "bridal", "emoji": "💛", "badge": "Bridal",          "price": 125000, "weight": "45g",  "purity": "22K",     "in_stock": True},
    {"id": 3,  "name": "Silver Filigree Jhumkas",  "category": "silver", "emoji": "✨", "badge": "Sterling Silver", "price": 3200,   "weight": "12g",  "purity": "925",     "in_stock": True},
    {"id": 4,  "name": "Gold Mangalsutra",         "category": "gold",   "emoji": "🔮", "badge": "22K Gold",        "price": 32000,  "weight": "10g",  "purity": "22K",     "in_stock": True},
    {"id": 5,  "name": "Custom Name Pendant",      "category": "custom", "emoji": "🛠️","badge": "Custom",          "price": 8500,   "weight": "4g",   "purity": "18K/22K", "in_stock": True},
    {"id": 6,  "name": "Silver Anklet Pair",       "category": "silver", "emoji": "🌙", "badge": "Sterling Silver", "price": 2800,   "weight": "20g",  "purity": "925",     "in_stock": True},
    {"id": 7,  "name": "Bridal Nath",              "category": "bridal", "emoji": "💍", "badge": "Bridal",          "price": 18000,  "weight": "6g",   "purity": "22K",     "in_stock": True},
    {"id": 8,  "name": "Gold Kada Bangle",         "category": "gold",   "emoji": "🌀", "badge": "22K Gold",        "price": 68000,  "weight": "25g",  "purity": "22K",     "in_stock": False},
    {"id": 9,  "name": "Silver Pooja Thali Set",   "category": "silver", "emoji": "🪔", "badge": "Sterling Silver", "price": 12500,  "weight": "80g",  "purity": "999",     "in_stock": True},
    {"id": 10, "name": "Custom Ring Design",       "category": "custom", "emoji": "💎", "badge": "Custom",          "price": 15000,  "weight": "5g",   "purity": "18K/22K", "in_stock": True},
    {"id": 11, "name": "Bridal Full Set",          "category": "bridal", "emoji": "👑", "badge": "Bridal",          "price": 285000, "weight": "110g", "purity": "22K",     "in_stock": True},
    {"id": 12, "name": "Silver Waist Chain",       "category": "silver", "emoji": "⛓️","badge": "Sterling Silver",  "price": 7800,   "weight": "35g",  "purity": "925",     "in_stock": True},
]

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def make_token(email: str) -> str:
    token = base64.urlsafe_b64encode(f"{email}:{uuid.uuid4()}".encode()).decode()
    SESSIONS[token] = email
    return token

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated")
    email = SESSIONS.get(creds.credentials)
    if not email or email not in USERS_DB:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return USERS_DB[email]

def optional_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not creds:
        return None
    email = SESSIONS.get(creds.credentials)
    return USERS_DB.get(email)


# ─────────────────────────────────────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────────────────────────────────────
class SignupRequest(BaseModel):
    first_name: str
    last_name: str = ""
    email: EmailStr
    phone: str = ""
    city: str = ""
    password: str = Field(min_length=8)

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class CartItem(BaseModel):
    id: int
    qty: int = Field(ge=1, le=20)

class CartUpsertRequest(BaseModel):
    items: List[CartItem]

class CheckoutRequest(BaseModel):
    items: List[dict]
    address: str = "Karnataka, India"
    promo_code: str = ""

class WishlistRequest(BaseModel):
    product_id: int


# ─────────────────────────────────────────────────────────────────────────────
# Auth endpoints
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/auth/signup", tags=["Auth"])
def signup(req: SignupRequest):
    if req.email in USERS_DB:
        raise HTTPException(status_code=400, detail="Email already registered.")
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "first_name": req.first_name,
        "last_name": req.last_name,
        "email": req.email,
        "phone": req.phone,
        "city": req.city,
        "password_hash": hash_password(req.password),
        "created_at": datetime.utcnow().isoformat(),
    }
    USERS_DB[req.email] = user
    CARTS_DB[user_id] = []
    WISHLIST_DB[user_id] = []
    token = make_token(req.email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {k: v for k, v in user.items() if k != "password_hash"}
    }


@app.post("/api/auth/signin", tags=["Auth"])
def signin(req: SigninRequest):
    user = USERS_DB.get(req.email)
    if not user or user["password_hash"] != hash_password(req.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    token = make_token(req.email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {k: v for k, v in user.items() if k != "password_hash"}
    }


@app.post("/api/auth/signout", tags=["Auth"])
def signout(creds: HTTPAuthorizationCredentials = Depends(security)):
    if creds and creds.credentials in SESSIONS:
        del SESSIONS[creds.credentials]
    return {"message": "Signed out successfully."}


@app.get("/api/auth/me", tags=["Auth"])
def get_me(user=Depends(get_current_user)):
    return {k: v for k, v in user.items() if k != "password_hash"}


# ─────────────────────────────────────────────────────────────────────────────
# Product endpoints
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/products", tags=["Products"])
def list_products(category: Optional[str] = None, in_stock: Optional[bool] = None):
    result = PRODUCTS
    if category:
        result = [p for p in result if p["category"] == category]
    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]
    return {"products": result, "total": len(result)}


@app.get("/api/products/{product_id}", tags=["Products"])
def get_product(product_id: int):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    related = [p for p in PRODUCTS if p["category"] == product["category"] and p["id"] != product_id][:4]
    return {"product": product, "related": related}


# ─────────────────────────────────────────────────────────────────────────────
# Cart endpoints
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/cart", tags=["Cart"])
def get_cart(user=Depends(get_current_user)):
    items = CARTS_DB.get(user["id"], [])
    enriched = []
    subtotal = 0
    for ci in items:
        p = next((p for p in PRODUCTS if p["id"] == ci["product_id"]), None)
        if p:
            line = {**p, "qty": ci["qty"], "subtotal": p["price"] * ci["qty"]}
            enriched.append(line)
            subtotal += line["subtotal"]
    shipping = 0 if subtotal >= 50000 else 299
    gst = round(subtotal * 0.03)
    return {
        "items": enriched,
        "subtotal": subtotal,
        "shipping": shipping,
        "gst": gst,
        "total": subtotal + shipping + gst,
        "item_count": sum(i["qty"] for i in items),
    }


@app.post("/api/cart/add", tags=["Cart"])
def add_to_cart(item: CartItem, user=Depends(get_current_user)):
    product = next((p for p in PRODUCTS if p["id"] == item.id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail="Product is out of stock.")
    cart = CARTS_DB.get(user["id"], [])
    idx = next((i for i, c in enumerate(cart) if c["product_id"] == item.id), None)
    if idx is not None:
        cart[idx]["qty"] = min(20, cart[idx]["qty"] + item.qty)
    else:
        cart.append({"product_id": item.id, "qty": item.qty})
    CARTS_DB[user["id"]] = cart
    return {"message": "Added to cart.", "cart_count": sum(c["qty"] for c in cart)}


@app.put("/api/cart/update", tags=["Cart"])
def update_cart(req: CartUpsertRequest, user=Depends(get_current_user)):
    cart = [{"product_id": i.id, "qty": i.qty} for i in req.items if i.qty > 0]
    CARTS_DB[user["id"]] = cart
    return {"message": "Cart updated.", "cart_count": sum(c["qty"] for c in cart)}


@app.delete("/api/cart/{product_id}", tags=["Cart"])
def remove_from_cart(product_id: int, user=Depends(get_current_user)):
    cart = [c for c in CARTS_DB.get(user["id"], []) if c["product_id"] != product_id]
    CARTS_DB[user["id"]] = cart
    return {"message": "Item removed.", "cart_count": sum(c["qty"] for c in cart)}


@app.delete("/api/cart", tags=["Cart"])
def clear_cart(user=Depends(get_current_user)):
    CARTS_DB[user["id"]] = []
    return {"message": "Cart cleared."}


# ─────────────────────────────────────────────────────────────────────────────
# Orders endpoint
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/orders/checkout", tags=["Orders"])
def checkout(req: CheckoutRequest, user=Depends(get_current_user)):
    if not req.items:
        raise HTTPException(status_code=400, detail="Cart is empty.")
    order_id = "MJO-" + str(uuid.uuid4())[:8].upper()
    subtotal = sum(i.get("price", 0) * i.get("qty", 1) for i in req.items)
    shipping = 0 if subtotal >= 50000 else 299
    gst = round(subtotal * 0.03)
    order = {
        "order_id": order_id,
        "user_id": user["id"],
        "user_email": user["email"],
        "items": req.items,
        "address": req.address,
        "subtotal": subtotal,
        "shipping": shipping,
        "gst": gst,
        "total": subtotal + shipping + gst,
        "status": "confirmed",
        "created_at": datetime.utcnow().isoformat(),
    }
    ORDERS_DB[order_id] = order
    CARTS_DB[user["id"]] = []
    return {
        "order_id": order_id,
        "total": order["total"],
        "status": "confirmed",
        "message": f"Order {order_id} placed successfully! We will contact you at {user.get('phone','your number')} for delivery.",
    }


@app.get("/api/orders", tags=["Orders"])
def get_orders(user=Depends(get_current_user)):
    orders = [o for o in ORDERS_DB.values() if o["user_id"] == user["id"]]
    return {"orders": sorted(orders, key=lambda o: o["created_at"], reverse=True)}


@app.get("/api/orders/{order_id}", tags=["Orders"])
def get_order(order_id: str, user=Depends(get_current_user)):
    order = ORDERS_DB.get(order_id)
    if not order or order["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order


# ─────────────────────────────────────────────────────────────────────────────
# Wishlist endpoints
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/wishlist", tags=["Wishlist"])
def get_wishlist(user=Depends(get_current_user)):
    ids = WISHLIST_DB.get(user["id"], [])
    products = [p for p in PRODUCTS if p["id"] in ids]
    return {"wishlist": products}


@app.post("/api/wishlist", tags=["Wishlist"])
def toggle_wishlist(req: WishlistRequest, user=Depends(get_current_user)):
    ids = WISHLIST_DB.get(user["id"], [])
    if req.product_id in ids:
        ids.remove(req.product_id)
        action = "removed"
    else:
        ids.append(req.product_id)
        action = "added"
    WISHLIST_DB[user["id"]] = ids
    return {"action": action, "product_id": req.product_id, "wishlist_count": len(ids)}


# ─────────────────────────────────────────────────────────────────────────────
# Metal prices proxy
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/metal-prices", tags=["Prices"])
def metal_prices():

    try:
        API_KEY = "YOUR_GOLDAPI_KEY"
        headers = {"x-access-token": API_KEY, "Content-Type": "application/json"}
        with httpx.Client(timeout=5) as client:
            gr = client.get("https://www.goldapi.io/api/XAU/INR", headers=headers)
            sr = client.get("https://www.goldapi.io/api/XAG/INR", headers=headers)
        if gr.status_code == 200 and sr.status_code == 200:
            gd, sd = gr.json(), sr.json()
            gpg = round(gd.get("price", 0) / 31.1035, 2)
            spg = round(sd.get("price", 0) / 31.1035, 2)
            return {
                "success": True,
                "gold":   {"price_per_gram": gpg, "price_per_10g": round(gpg*10, 2), "currency": "INR", "change": round(gd.get("ch",0)/31.1035,2), "change_percent": round(gd.get("chp",0),2)},
                "silver": {"price_per_gram": spg, "price_per_10g": round(spg*10, 2), "currency": "INR", "change": round(sd.get("ch",0)/31.1035,2), "change_percent": round(sd.get("chp",0),2)},
                "last_updated": gd.get("timestamp"), "source": "goldapi.io"
            }
    except Exception as e:
        pass
    return {
        "success": True,
        "gold":   {"price_per_gram": 7250.0, "price_per_10g": 72500.0, "currency": "INR", "change": 0, "change_percent": 0},
        "silver": {"price_per_gram": 88.5,   "price_per_10g": 885.0,   "currency": "INR", "change": 0, "change_percent": 0},
        "last_updated": None, "source": "fallback", "note": "Live prices temporarily unavailable."
    }


# ─────────────────────────────────────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["System"])
def health():
    return {"status": "ok", "service": "mayin Jewellery API", "version": "1.0.0"}
