import json
from . models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']
    for i in cart:
        try:
            product = Product.objects.get(id=1)
            cartItems += cart[i]['quantity']
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

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
    return {'items': items, 'order': order, 'cartItems': cartItems}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        cartItems = cookieData['cartItems']
        order = cookieData['order']
    return {'cartItems': cartItems, 'items': items, 'order': order}

