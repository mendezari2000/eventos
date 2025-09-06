from django.urls import include, path
from django.contrib import admin
from app.views import NotificationListView, TicketListView
from eventos import settings

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("app.urls")),
    path('panel/', include('panel_admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
