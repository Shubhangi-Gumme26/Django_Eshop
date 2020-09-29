from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from Eshop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", RedirectView.as_view(url="store/")),
    path("store/", include("store.urls")),
]  +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


