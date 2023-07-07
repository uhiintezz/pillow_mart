from django.shortcuts import render
from django.views.generic import ListView



def home(request):
    return render(request, 'base.html')


def mart(request):
    return render(request, 'mart/mart_list.html')


