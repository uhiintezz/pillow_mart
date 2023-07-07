# Generated by Django 4.1.3 on 2023-04-15 05:55

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0009_alter_about_is_published_alter_about_mini_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='is_published',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='about',
            name='mini_text',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='about',
            name='our_mission',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='about',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='about',
            name='text_subscription',
            field=ckeditor.fields.RichTextField(),
        ),
    ]