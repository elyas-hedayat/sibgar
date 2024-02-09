from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('apps.api.urls'), name='api'),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns = urlpatterns + [path("__debug__/", include("debug_toolbar.urls"))]
