from django import template
from django.utils import timezone
import datetime
from blog.models import Category, Tag, Post


register = template.Library()


@register.inclusion_tag('blog/tags/right_menu.html')
def get_categories():
    category = Category.objects.all()
    return {'list_category': category}


@register.simple_tag()
def get_tags(post):
    return Tag.objects.filter(posts=post.pk)


@register.simple_tag()
def get_all_tags():
    return Tag.objects.all()

@register.inclusion_tag('blog/tags/recent_post.html')
def get_recent(cnt=4):
    posts = Post.objects.order_by('-pk')[:cnt]
    return {'posts': posts, 'now_date': timezone.now()}


@register.filter
def hours_ago(time, hours):
    return time + datetime.timedelta(hours=hours) > timezone.now()

@register.inclusion_tag('blog/tags/search_nav.html')
def search_field():
    return {}


@register.inclusion_tag('blog/tags/right_menu.html')
def get_categories():
    category = Category.objects.all()
    return {'list_category': category}


