from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . forms import *
from . utils import *
import json
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from . models import Customer

def home(request):
    return render(request, 'base.html')


def mart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'order': order, 'items': items, 'cartItems': cartItems}
    return render(request, 'mart/mart_list.html', context)


def product(request, product_slug):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    product = Product.objects.get(slug=product_slug)
    context = {'product': product, 'cartItems': cartItems, 'order': order, 'items': items,}
    return render(request, 'mart/product_detail.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data['quantity']

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + quantity)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - quantity)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'mart/cart.html', context)

def checkout(request):
    return render(request, 'mart/checkout.html',)

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mart/login.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Авторизация")
    #     return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)

        return super().form_valid(form)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'mart/register.html'
    success_url = reverse_lazy('login')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Регистрация")
    #     return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        user = form.save()

        name = form.cleaned_data['username']
        email = form.cleaned_data['email']

        Customer.objects.create(user=user, name=name, email=email)
        login(self.request, user)
        return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('login')