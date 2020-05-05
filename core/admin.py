from django.contrib import admin

from .models import Item, OrderItem, Order, Category, Brand

# admin.site.register(Item)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category',
                    'brand', 'color', 'label')
    # list_filter
    list_editable = ('title', 'color', 'category', 'price', 'brand', )


admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Brand)
admin.site.register(Category)
