# Generated by Django 4.1.3 on 2023-07-17 19:21

import ckeditor.fields
import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('our_mission', ckeditor.fields.RichTextField()),
                ('text', ckeditor.fields.RichTextField()),
                ('mini_text', ckeditor.fields.RichTextField()),
                ('text_subscription', ckeditor.fields.RichTextField()),
                ('is_published', models.BooleanField()),
                ('website', models.URLField(default='https://www.youtube.com/watch?v=DWHB6nTyKDI')),
            ],
        ),
        migrations.CreateModel(
            name='AboutSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='ContactLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('mini_text', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(code='invalid', flags=re.RegexFlag['IGNORECASE'], inverse_match=False, message='Поставьте точку в конце!', regex='')])),
                ('email', models.EmailField(max_length=100, validators=[django.core.validators.EmailValidator(message='Введите корректный email!!!')])),
                ('website', models.URLField(max_length=250)),
                ('message', models.TextField(max_length=5000)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.FileField(upload_to='icons/')),
                ('name', models.CharField(max_length=200)),
                ('link', models.URLField()),
            ],
        ),
    ]
