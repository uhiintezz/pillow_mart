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
import datetime


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
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    if isinstance(order, dict):
        subtotal = order['get_cart_total']
    else:
        subtotal = order.get_cart_total

    shipping_cost = 0

    if isinstance(order, dict):
        shipping = order['shipping']
    else:
        shipping = order.shipping

    if shipping == True:
        shipping_cost = 50

    total = subtotal + shipping_cost

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'total': total, 'shipping_cost': shipping_cost}
    return render(request, 'mart/checkout.html', context)

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

        customer, created = Customer.objects.get_or_create(
            name=name, email=email
        )


        customer.user = user
        customer.save()

        login(self.request, user)

        return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('login')


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    order.transaction_id = transaction_id
    if float(data['form']['total']) == float(order.get_cart_total) + float(data['shipping_cost']):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse("Procces complete", safe=False)