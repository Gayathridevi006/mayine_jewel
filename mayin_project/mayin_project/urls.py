"""
URL configuration for mayin_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
app = 'mayin'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',                          views.home,           name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/',                     views.cart,           name='cart'),
    path('signin/',                   views.signin,         name='signin'),
    path('signup/',                   views.signup,         name='signup'),
    path('custom-order/',             views.custom_order,   name='custom_order'),
    path('api/metal-prices/',         views.get_metal_prices, name='metal_prices'),
        path('',                          views.home,           name='home'),
    path('collections/',              views.collections,    name='collections'),
    path('bridal/',                   views.bridal,         name='bridal'),
    path('wishlist/',                 views.wishlist,       name='wishlist'),
    path('orders/',                   views.orders,         name='orders'),
    path('track/',                    views.track_order,    name='track_order'),
    path('support/',                  views.support,        name='support'),
    path('about/',                    views.about,          name='about'),
]


