from django.views.generic import TemplateView, ListView, DetailView
from .models import Event, Notification, Category

class NotificationListView(ListView):
    model = Notification
    template_name = "app/notification.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.all().order_by("priority")

class HomeView(TemplateView):
    model = Category
    template_name = "home.html"


class EventListView(ListView):
    model = Event
    template_name = "app/events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all().order_by("date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "app/event_detail.html"
    context_object_name = "event"
