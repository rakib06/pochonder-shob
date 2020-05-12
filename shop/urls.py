from django.urls import path
from .views import (
    ShopLoginView, calendarView

)

app_name = 'shop'

urlpatterns = [
    path('service-and-shop/', ShopLoginView.as_view(), name='home'),
    path('c/', calendarView.as_view(), name='calendar'),
    # path('checkout/', CheckoutView.as_view(), name='checkout'),
    # extra add

]
