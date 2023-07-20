from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('mart/', mart, name='mart'),
    path('cart/', cart, name='cart'),
    path('update_item/', updateItem, name='update_item'),
    path('product/<slug:product_slug>', product, name='product'),
]