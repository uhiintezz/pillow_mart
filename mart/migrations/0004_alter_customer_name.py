# Generated by Django 4.1.3 on 2023-07-24 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0003_alter_customer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
