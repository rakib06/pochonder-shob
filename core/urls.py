from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url

from django.views.static import serve

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
    MarketsView,
    MarketsView1,
    ShopsView,
    ProductsView,
    get_items,
    # RequestRefundView,
    add_item, add_shop,
    CustomerOrderStatusView,
    get_shop_cat_items,
    home_view,
    side_bar,
    get_shops,

)
app_name = 'core'

urlpatterns = [
    # path('all', HomeView.as_view(), name='home'),
    # path('', ShopsView.as_view(), name='shops'),
    # path('', home_view, name='home'),
    path('', MarketsView.as_view(), name='markets'),
    # path('markets/', MarketsView.as_view(), name='markets'),
    path('shops/', ShopsView.as_view(), name='shops'),
    path('products/', ProductsView.as_view(), name='products'),

    path('markets/', MarketsView1.as_view(), name='markets'),

    path('shop-items/<id>/', get_items, name='shop-items'),
    path('area/<id>/', get_shops, name='area-shops'),
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
    url(r'^image/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
