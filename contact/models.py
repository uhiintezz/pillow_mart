import re
from django import forms
from ckeditor.fields import RichTextField
from django.db import models
from django.core.validators import (
    RegexValidator,
    EmailValidator,
)




class ContactModel(models.Model):
    '''Класс модели обратной связи'''
    name = models.CharField(max_length=50, validators=[
        RegexValidator(
            regex=r'',
            message='Поставьте точку в конце!',
            code='invalid',
            inverse_match=False,
            flags=re.IGNORECASE
        )
    ])
    email = models.EmailField(max_length=100, validators=[
        EmailValidator(
            message='Введите корректный email!!!'
        )
    ])
    website = models.URLField(max_length=250)
    message = models.TextField(max_length=5000)
    create_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.name} - {self.email}'


class ContactLink(models.Model):
    ''' Класс модели контактов '''
    title = models.CharField(max_length=200)
    mini_text = RichTextField()

    def __str__(self):
        return self.title



class About(models.Model): #Event
    '''Класс модели страницы о нас'''
    our_mission = RichTextField()
    text = RichTextField()
    mini_text = RichTextField()
    text_subscription = RichTextField()
    is_published = models.BooleanField()
    website = models.URLField(default='https://www.youtube.com/watch?v=DWHB6nTyKDI')

class AboutSubscription(models.Model):
    '''Класс модели подписки'''
    email = models.EmailField()




class Social(models.Model):
    '''Класс модели соц сетей страницы о нас'''
    icon = models.FileField(upload_to='icons/')
    name = models.CharField(max_length=200)
    link = models.URLField()


    def __str__(self):
        return self.name




