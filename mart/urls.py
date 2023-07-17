from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('mart/', mart, name='mart'),
    path('product/<slug:product_slug>', product, name='product')
]