# Generated by Django 4.1.3 on 2022-12-27 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_alter_contactmodel_email_alter_contactmodel_website'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactlink',
            name='icon',
        ),
    ]