from django.shortcuts import render
from . utils import *



def home(request):
    return render(request, 'base.html')


def mart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'mart/mart_list.html', context)


def product(request, product_slug):
    data = cartData(request)
    cartItems = data['cartItems']
    product = Product.objects.get(slug=product_slug)
    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'mart/product_detail.html', context)


