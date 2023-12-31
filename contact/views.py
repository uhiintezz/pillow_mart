from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm, AboutSubscriptionForm
from django.http import Http404
from django.contrib import messages
from .models import *
from .utils import cartData




def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            print('save')
            return redirect('home')
        else:
            print('---------------------')
            print(form)
            print(form.errors)
            print(form.cleaned_data)

    else:
        form = ContactForm()

    c1 = ContactLink.objects.get(pk=1)
    c2 = ContactLink.objects.get(pk=2)
    c3 = ContactLink.objects.get(pk=3)
    return render(request, 'contact/contact.html', {'form': form, 'c1': c1, 'c2': c2, 'c3': c3, 'cartItems': cartItems})



def about(request):
    if request.method == 'POST':
        form = AboutSubscriptionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            object = form.save()
            return redirect('home')
        else:
            form = AboutSubscriptionForm()
            try:
                object = About.objects.get(is_published=True)
                data = cartData(request)
                cartItems = data['cartItems']
                return render(request, 'contact/about.html',
                              context={'object': object, 'form': form, 'cartItems': cartItems, 'error': 'email is not valid'})
            except About.MultipleObjectsReturned:
                raise Http404("You have selected several objects")
            except About.DoesNotExist:
                raise Http404("You have not selected object")
    else:
        form = AboutSubscriptionForm()
        try:
            object = About.objects.get(is_published=True)
            data = cartData(request)
            cartItems = data['cartItems']
            return render(request, 'contact/about.html', context={'object': object, 'form': form, 'cartItems': cartItems})
        except About.MultipleObjectsReturned:
            raise Http404("You have selected several objects")
        except About.DoesNotExist:
            raise Http404("You have not selected object")




