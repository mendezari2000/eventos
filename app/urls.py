from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (
    HomeView,
    RegisterView,
    LoginView,
    EventListView,
    EventDetailView,
    EventDeleteView,
    EventFormView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("events/", EventListView.as_view(), name="events"),
    path("events/create/", EventFormView.as_view(), name="event_form"),
    path("events/<int:id>/edit/", EventFormView.as_view(), name="event_edit"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("events/<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
]
