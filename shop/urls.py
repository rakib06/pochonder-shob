from django.urls import path
from .views import (
    ShopLoginView, IndexView, ShopProfile

)


app_name = 'shop'

urlpatterns = [
    path('service-and-shop/', ShopLoginView.as_view(), name='home'),
    path('c/', IndexView.as_view(), name='calendar'),
    path('profile/', ShopProfile, name='shop-profile'),
    # path('checkout/', CheckoutView.as_view(), name='checkout'),
    # extra add

]
