"""litreview URL Configuration


"""
from django.urls import path, include
from django.contrib import admin

# media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("review.urls")),
]
# lowtech file storage solution for academic purpose & money wise
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [
    #     path("__debug__/", include("debug_toolbar.urls")),
    # ]


urlpatterns += [
    path("review/", include("review.urls")),
    path("authentication/", include("authentication.urls")),
]
