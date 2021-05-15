from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("luqman/", admin.site.urls),
    path("", include("search.urls")),
    path("diary/", include("diary.urls")),
    path("weather/", include("weather.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
