"""URL configuration for the DjangoSIGE project."""

import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("djangosige.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        *urlpatterns,
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        path("__debug__/", include(debug_toolbar.urls)),
    ]
