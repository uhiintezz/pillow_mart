from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse





class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'




class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    image = models.ImageField(upload_to='articles/')
    text = RichTextField()
    category = models.ForeignKey(
        Category,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True
    )
    tags = models.ManyToManyField('Tag', related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_single', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'



class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Comment(models.Model):
    name = models.CharField(max_length=100)
    write_comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=150, blank=True, null=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



