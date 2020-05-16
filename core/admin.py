from django.contrib import admin

from .models import (Item, OrderItem, Order, Shop, Coupon,
                     Refund, Address, UserProfile, Category, Label, ShopType)
from django.contrib.contenttypes.admin import GenericTabularInline


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'item', 'get_total_item_price',
                    'get_total_discount_item_price', 'get_final_price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',

                    # 'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',

        # 'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


'''
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',


        'default'
    ]
    list_filter = ['default']
    search_fields = ['user', 'street_address', 'apartment_address', ]

'''


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = ['image_tag', 'title', 'price',
                    'discount_price', 'category', ]

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        exclude_set = set()
        if obj:  # obj will be None on the add page, and something on change pages
            exclude_set.add('slug')
        return [f for f in fields if f not in exclude_set]

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or []  # get overall excluded fields

        if request.user.is_superuser:  # if user is not a superuser
            return excluded + ['slug']

        return excluded

    # sudhu matro tar shop er item gulo e dekhabe
    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:

            return qs

        qs1 = Shop.objects.get(user=request.user.id)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>', qs)
        # return qs.filter(shop=request.shop.id)
        return qs.filter(shop=qs1)


# admin.site.register(Item, ItemAdmin)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):

    list_display = ['image_tag', 'title', 'get_category']

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or []  # get overall excluded fields

        if not request.user.is_superuser:  # if user is not a superuser
            return excluded + ['slug']

        return excluded

    # sudhu matro tar shop er item gulo e dekhabe
    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:

            return qs

        # return qs.filter(shop=request.shop.id)
        return qs.filter(user=request.user.id)


admin.site.register(Order, OrderAdmin)
# admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
# admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Label)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShopType)
