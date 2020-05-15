from django.urls import path
from .views import IndexView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'


urlpatterns = [
    # path('home/', views.ShopProfile.as_view(), name='home'),

    path('checkout/', IndexView.as_view(),
         name='checkout'),    # extra add

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
