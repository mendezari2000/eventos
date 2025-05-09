from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Event, User
import datetime


class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register.html", {})

    def post(self, request):
        email = request.POST.get("email")
        username = request.POST.get("username")
        is_organizer = request.POST.get("is-organizer") is not None
        password = request.POST.get("password")
        password_confirm = request.POST.get("password-confirm")

        errors = User.validate_new_user(email, username, password, password_confirm)

        if errors:
            return render(
                request,
                "accounts/register.html",
                {"errors": errors, "data": request.POST},
            )

        user = User.objects.create_user(
            email=email, username=username, password=password, is_organizer=is_organizer
        )
        login(request, user)
        return redirect("events")


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(
                request,
                "accounts/login.html",
                {"error": "Usuario o contraseña incorrectos"},
            )

        login(request, user)
        return redirect("events")


class HomeView(TemplateView):
    template_name = "home.html"


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "app/events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all().order_by("scheduled_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_is_organizer"] = self.request.user.is_organizer
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "app/event_detail.html"
    context_object_name = "event"


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = "app/event_confirm_delete.html"
    success_url = reverse_lazy("events")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(
            request.user, "is_organizer", False
        ):
            return redirect("events")
        return super().dispatch(request, *args, **kwargs)


class EventFormView(LoginRequiredMixin, View):
    template_name = "app/event_form.html"

    def get(self, request, id=None):
        user = request.user
        if not user.is_organizer:
            return redirect("events")

        event = get_object_or_404(Event, pk=id) if id else {}
        return render(
            request,
            self.template_name,
            {"event": event, "user_is_organizer": request.user.is_organizer},
        )

    def post(self, request, id=None):
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        time = request.POST.get("time")

        year, month, day = map(int, date.split("-"))
        hour, minutes = map(int, time.split(":"))

        scheduled_at = timezone.make_aware(
            datetime.datetime(year, month, day, hour, minutes)
        )

        if id is None:
            Event.new(title, description, scheduled_at, request.user)
        else:
            event = get_object_or_404(Event, pk=id)
            event.update(title, description, scheduled_at, request.user)

        return redirect("events")
