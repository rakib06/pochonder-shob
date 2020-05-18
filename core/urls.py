from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ItemDetailView,
    CheckoutView,
    # HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    # PaymentView,
    AddCouponView,
    ShopCreate,
    ShopsView,
    get_items,
    # RequestRefundView,
    add_item, add_shop,
    CustomerOrderStatusView,
    get_shop_cat_items,
    home_view,
    side_bar
)
app_name = 'core'

urlpatterns = [
    # path('all', HomeView.as_view(), name='home'),
    # path('', ShopsView.as_view(), name='shops'),
    path('', home_view, name='home'),

    path('shop-items/<id>/', get_items, name='shop-items'),
    path('shops-cat/<id>', get_shop_cat_items,
         name='shops-cat'),
    path('offer-shop/<id>', get_shop_cat_items,
         name='shops-offer'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('shop/add/', ShopCreate.as_view(), name='add-shop'),
    path('order/', CustomerOrderStatusView.as_view(), name='customer-order'),

    # path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    # path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    url(r'^uploads/simple/$', add_shop, name='add_shop'),
    url(r'^uploads/form/$', add_item, name='add_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
