from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib import admin
from .views import (
    CompraExitosaView,
    HomeView,
    EventListView,
    EventDetailView,
    NotificationListView,
    TicketListView,
    RegisterView,
    ProfileView,
    LogoutView,

)
from app import views

urlpatterns = [
    path('compra-exitosa/<int:event_id>/', CompraExitosaView.as_view(), name='compra_exitosa'),
    path('comprar/<int:event_id>/', views.ComprarTicketView.as_view(), name='comprar_ticket'),
    path("", HomeView.as_view(), name="home"),
    path("events/", EventListView.as_view(), name="events"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("notificaciones/", NotificationListView.as_view(), name="notifications"),
    path("tickets/", TicketListView.as_view(), name = "tickets"),
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path('events/<int:pk>/buy/', EventDetailView.as_view(), name='buy_ticket'),
    path('admin/', admin.site.urls),
]
