from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Social._meta.fields]
    list_display.append('get_icon')
    readonly_fields = ('get_icon',)

    def get_icon(self, obj):
        return mark_safe(f'<img src={obj.icon.url} width="50" height="50"')



@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'create_at')
    readonly_fields = ('create_at',)
    search_fields = ('name',)



@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'mini_text']
    search_fields = ('title',)



@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_published', 'website']
    list_display_links = ['id', 'website']
    list_editable = ('is_published',)
    save_on_top = True


class AboutSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    list_display_links = ['id', 'email']

admin.site.register(AboutSubscription, AboutSubscriptionAdmin)









