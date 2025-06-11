from django.views.generic import TemplateView, ListView, DetailView
from .models import Event, Notification, Category, Ticket
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

class LoginView(TemplateView):
    template_name = "app/login.html"
    context_object_name = "login"

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})
    
class LogoutView(TemplateView):
    template_name = "logout.html"
    context_object_name = "logout"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class RegisterView(TemplateView):
    template_name = "register.html"
    context_object_name = "register"
    
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})
    

class TicketListView(ListView):
    model = Ticket
    template_name = "app/tickets.html"
    context_object_name = "tickets"    

    def get_queryset(self):
        queryset = Ticket.objects.all().order_by("buy_date")
        for ticket in queryset:
            ticket.total = ticket.prize * ticket.quantity
        return queryset


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
