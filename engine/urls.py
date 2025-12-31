from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


static_path_media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_path = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('userauth.urls')),
    path('nominee/', include('nominee.urls')),
    path('sys/', include('voting.urls')),
    path('ioauth/', include('allauth.urls')),
] + static_path + static_path_media

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)