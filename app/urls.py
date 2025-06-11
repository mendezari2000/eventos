from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    NotificationListView,
    TicketListView,
    RegisterView,
    ProfileView
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("events/", EventListView.as_view(), name="events"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("notificaciones/", NotificationListView.as_view(), name="notifications"),
    path("tickets/", TicketListView.as_view(), name = "tickets"),
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
]
