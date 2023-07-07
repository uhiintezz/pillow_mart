from django.urls import path
from .views import *


urlpatterns = [
    path('contact/', contact, name='contact'),
    path('about/', about, name='about')
]


