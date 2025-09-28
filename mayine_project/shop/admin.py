from django.contrib import admin

# Register your models here.
from .models import Category, Product, CustomerProfile, Cart, CartItem, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('category', 'is_active')


admin.site.register(CustomerProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)