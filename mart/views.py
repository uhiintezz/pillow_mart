from django.shortcuts import render




def home(request):
    return render(request, 'base.html')


def mart(request):
    return render(request, 'mart/mart_list.html')

def product(request):
    return render(request, 'mart/product_detail.html')


