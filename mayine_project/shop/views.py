# shop/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Category, Product, Cart, CartItem


class HomeView(TemplateView):
    template_name = "shop/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        segment_slugs = [
            "earrings", "chains", "customised-jewellery",
            "dollars", "rings", "leg-chains"
        ]
        segments = []
        for slug in segment_slugs:
            cat = Category.objects.filter(slug=slug).first()
            if cat:
                segments.append({
                    "category": cat,
                    "products": cat.products.filter(is_active=True)[:8],
                })
        ctx["segments"] = segments
        ctx["featured"] = Product.objects.filter(is_active=True).order_by("-created_at")[:8]
        return ctx


class CategoryListView(ListView):
    model = Product
    template_name = "shop/category_list.html"
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Product.objects.filter(category=self.category, is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = self.category
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"


@login_required
def add_to_cart(request, product_id):
    """Add a product to the current user's cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)

    # get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # check if product already in cart
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return redirect("shop:view_cart")


@login_required
def view_cart(request):
    """Display the cart items for the current user"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product")
    total = sum([i.line_total() for i in items])
    return render(request, "shop/cart.html", {"cart": cart, "items": items, "total": total})


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from cart"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("shop:view_cart")



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # log them in immediately
            return redirect("shop:home")  # go to home page
    else:
        form = UserCreationForm()
    return render(request, "shop/register.html", {"form": form})

# End of shop/views.py