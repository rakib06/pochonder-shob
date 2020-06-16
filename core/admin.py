from django.contrib import admin
from django.urls import reverse
from .models import (Item, OrderItem, Order, Shop, Coupon,
                     Refund, Address, UserProfile, Category, Offer, ShopType, Area, RootCat, Size, Slider)
from django.contrib.contenttypes.admin import GenericTabularInline


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item_image',
                    'item', 'quantity', 'quantity_available', 'ordered', 'get_final_price']
    list_select_related = True
    ordering = ("ordered",)
    list_editable = ['ordered', 'quantity_available']

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:

            return qs

        qs1 = Shop.objects.get(user=request.user.id)
        items = Item.objects.filter(shop=qs1.id)
        qs2 = OrderItem.objects.filter(item__in=items)

        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>', qs1, items, qs2)
        # return qs.filter(shop=request.shop.id)
        return qs2
        # return qs.filter(shop=qs1)

    def item_image(self, obj):
        return obj.item.image_test

    list_display_links = ('item',)


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
@admin.register(ShopType)
class ShopType(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = ['image_tag', 'title', 'in_stock',
                    'price', 'discount_price', 'category', 'description', 'created_at', 'updated_at']

    list_editable = ['in_stock', 'title', 'category', 'in_stock', 'description',
                     'price', 'discount_price', ]

    search_fields = [
        'title','category__name',]



    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.list_display = ('image_tag', 'title', 'price',
                                 'discount_price', 'category',)
        return super().changelist_view(request, extra_context)

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
    ordering = ('-created_at',)
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

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):

    list_display = ['image_tag', 'name', 'created_at', 'updated_at']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):

    list_display = ['image_tag', 'title', 'get_category']
    prepopulated_fields = {"slug": ("title",)}
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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['items', 'customer_name', 'comment', 'mobile_number', 'shipping_address',
              'user', 'ordered', 'being_packed', 'being_delivered', 'received', 'created_at', 'updated_at']

    list_display = ['get_products', 'customer_name', 'comment', 'mobile_number', 'shipping_address',
                    'ordered', 'being_packed', 'being_delivered', 'received',  'user', 'created_at', 'updated_at']
    list_editable = ['being_packed', 'being_delivered', 'received']

    def get_products(self, obj):
        return ", ".join([str(p.item.title) + " = " + str(p.quantity) + " Shop ID = " + str(p.item.shop.id) for p in obj.items.all()])

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or []  # get overall excluded fields

        if not request.user.is_superuser:  # if user is not a superuser
            return excluded + ['mobile_number']

        return excluded


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):

    list_display = ['image_tag', 'caption', 'created_at', 'updated_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['id','name', 'slug', 'tags']
    list_editable = ['name', 'slug', 'tags']
    list_display_links = ('id',)

@admin.register(RootCat)
class RootCatAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("name",)}
    list_display = ['id','title', ]
    list_editable = [ 'title']
    list_display_links = ('id',)
# admin.site.register(Order, OrderAdmin)
# admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
# admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
#admin.site.register(Category)
admin.site.register(Offer)
# admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Size)



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    fields = ['user', 'item', 'ordered',
                'created_at', 'updated_at', 'quantity_available']

    list_display = ['image_tag', 'user', 'item', 'ordered',
                'created_at', 'updated_at', 'quantity_available' ]
  
   