from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.decorators.cache import never_cache
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("products.urls")),
    url(
        r"^media/(?P<path>.*)$",
        never_cache(serve),
        {"document_root": settings.MEDIA_ROOT},
    ),
    url(
        r"^static/(?P<path>.*)$",
        never_cache(serve),
        {"document_root": settings.STATIC_ROOT},
    ),
]
