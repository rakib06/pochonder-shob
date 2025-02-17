from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
admin.site.site_header = 'Pochonder-Shob.com'
admin.site.site_title = 'Pochonder-Shob.com'
admin.site.index_title = "Welcome to Pochonder-Shob.com"

urlpatterns = [
    path('shop/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
