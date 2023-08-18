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
    data = cartData(request)
    cartItems = data['cartItems']
    items = Product.objects.all()[:6]
    return render(request, 'base.html', {'items': items, 'cartItems': cartItems})


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



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mart/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        cartItems = data['cartItems']
        context['cartItems'] = cartItems
        return context

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        cartItems = data['cartItems']
        context['cartItems'] = cartItems
        return context

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
        auth = True
    else:
        customer, order = guestOrder(request, data)
        auth = False

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
    return JsonResponse({'auth': auth, 'transaction_id': transaction_id, 'total': data['form']['total'], 'subtotal': order.get_cart_total}, safe=False)


def confirmation(request):
    try:
        shipping = json.loads(request.COOKIES.get('SHIPPING'))
        order = json.loads(request.COOKIES.get('MY_ORDER'))
        creation_time = order['creation_time'][:10]
        method = order['method']
        if request.user.is_authenticated:
            customer = request.user.customer
            orders = [ i['transaction_id'] for i in Order.objects.filter(customer=customer, complete=True).values('pk', 'transaction_id').order_by('-pk') ]
            items = Order.objects.get(transaction_id=orders[0], complete=True, customer=customer).orderitem_set.all()

            if len(orders) > 6:
                orders = orders[:6]
        else:
            orders = json.loads(request.COOKIES.get('TRANSACTION_IDS'))[::-1]
            cart = order['cart']
            items = []
            for i in cart:
                try:
                    product = Product.objects.get(id=i)
                    total = (product.price * cart[i]['quantity'])

                    item = {
                        'product': {
                            'id': product.id,
                            'name': product.name,
                            'price': product.price,
                            'imageURL': product.imageURL
                        },
                        'quantity': cart[i]['quantity'],
                        'get_total': total,
                    }

                    items.append(item)
                except:
                    pass

            if len(orders) > 6:
                orders = orders[:6]

        data = cartData(request)
        cartItems = data['cartItems']

        context = {'orders': orders, 'order': order, 'cartItems': cartItems, 'items': items, 'style': True, 'creation_time': creation_time, 'method': method}

        if shipping['shipping'] == 'True':
            context['shipping'] = True
            context['shippingInfo'] = shipping['shippingInfo']
        else:
            context['shipping'] = False

        return(render(request, 'mart/confirmation.html', context))
    except:
        data = cartData(request)
        cartItems = data['cartItems']
        return (render(request, 'mart/confirmation.html', {'style': False, 'cartItems': cartItems}))


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


def elements(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return (render(request, 'mart/elements.html', {'cartItems': cartItems}))