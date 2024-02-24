
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path ('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('users/', include('users.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('contact/', include('contact.urls')),
    path('chat/', include('chat.urls')),
    path('news/', include('news.urls')),
    path('search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)