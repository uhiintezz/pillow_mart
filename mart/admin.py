from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'price', 'get_image']
    readonly_fields = ('get_image',)


    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="110" height="80"')



admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
