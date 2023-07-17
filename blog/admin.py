from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import *


class PostInline(admin.StackedInline):
    model = Post
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'category', 'author', 'created_at', 'id', 'get_image']
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="110" height="80"')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    inlines = [PostInline]
    search_fields = ('title',)



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'website', 'created_at', 'id']


