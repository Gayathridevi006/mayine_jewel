from django.urls import path
from .views import HomeView, CategoryListView, ProductDetailView, add_to_cart, view_cart, remove_from_cart, register
from django.contrib.auth import views as auth_views

app_name = "shop"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("category/<slug:slug>/", CategoryListView.as_view(), name="category"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("cart/", view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("register/", register, name="register"),

    # Login / Logout
    path('accounts/login/',
         auth_views.LoginView.as_view(
             template_name='shop/login.html',
             redirect_authenticated_user=True
         ),
         name='login'),
    path('accounts/logout/',
         auth_views.LogoutView.as_view(next_page='shop:home'),
         name='logout'),
]
