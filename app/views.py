from urllib import request
import uuid
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, View, CreateView, UpdateView
from .models import Event, Notification, Category, Ticket, User, RefundRequest, Comment, Rating
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from .forms import RefundRequestForm, CustomUserCreationForm, RatingForm
from django.db.models import Avg

class CommentView(View):
    model= Comment
    template_name= 'app/event_detail.html'
    context_object_name='comentarios'

class CompraExitosaView(View):
    template_name='app/confirmar_compra.html'
    context_object_name='compra_exitosa'

    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        return render(request, "app/confirmar_compra.html", {"event": event})
    
    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        tipo = request.POST.get("tipo")
        cantidad_str = request.POST.get("cantidad")  # puede venir como string vacío
        nro_tarjeta = request.POST.get('nro_tarjeta')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        cv_code = request.POST.get('cv_code')


        errors = {}

        
        try:
            cantidad = int(cantidad_str) if cantidad_str else 1
        except ValueError:
            errors["cantidad"] = "Cantidad inválida"
            return render(request, self.template_name, {
                "event": event,
                "errors": errors,
                "tipo": tipo,
                "cantidad": cantidad_str
            })

        ticket_code = str(uuid.uuid4())[:8]


        precio_unitario = event.prize
        if tipo == "VIP":
            precio_unitario = event.precio_vip

        total = precio_unitario * cantidad

        Ticket.objects.create(
            ticket_code=ticket_code,
            quantity=cantidad,  
            type_ticket=tipo,
            prize=precio_unitario,
            total=total,
            user=request.user,
            event=event
        )
        return redirect('compra_exitosa', event_id=event_id)

class ComprarTicketView(View):
    template_name="app/compratickets.html"
    context_object_name = "comprar_ticket"
    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        return render(request, "app/compratickets.html", {"event": event})

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)       
        return redirect('comprar_ticket', event_id=event.id)  


class LoginView(TemplateView):
    template_name = "app/login.html"
    context_object_name = "login"

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login (request, user)
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
    
class LogoutView(View):
    template_name = "home.html"
    context_object_name = "logout"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('categories')
   
class RegisterView(TemplateView):
    template_name = "app/register.html"
    context_object_name = "register"
    
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})
    

class TicketListView(ListView):
    model = Ticket
    template_name = "app/tickets.html"
    context_object_name = "tickets"    

    def get_queryset(self):
        queryset = Ticket.objects.filter(user=self.request.user).order_by("buy_date")
        for ticket in queryset:
            ticket.total = ticket.prize * ticket.quantity
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # esto es para mostrar el boton de reembolso solo si el evento ya pasó
        context['now'] = timezone.now()
        # esto es para mostrar el boton solo si hay una solicitud de reembolso pendiente
        for ticket in context['tickets']:
            refund = RefundRequest.objects.filter(ticket_code=ticket.ticket_code).order_by('-created_at').first()
            if refund:
                if refund.resolved:
                    if refund.approved:
                        ticket.refund_status = "Tu reembolso fue aprobado."
                    elif refund.rejected:
                        ticket.refund_status = "Tu reembolso fue rechazado."
                else:
                    ticket.refund_pending = True
            else:
                ticket.refund_pending = False
        return context



class NotificationListView(ListView):
    model = Notification
    template_name = "app/notification.html"
    context_object_name = "notifications"

    def get_queryset(self):
        #lista de notificaciones del usuario
        return Notification.objects.filter(users=self.request.user).order_by("priority", "-created_at")
    

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")  # <- capturamos el id si viene en la URL
        if pk:
            context["selected_notification"] = Notification.objects.filter(
                pk=pk, users=self.request.user
            ).first()
        else:
            context["selected_notification"] = None
        return context

        user = self.request.user
        # Solo las notificaciones asignadas a este usuario
        return Notification.objects.filter(users=user).order_by("priority", "-created_at")


class HomeView(TemplateView):
    model = Category
    template_name = "home.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CategoryView(ListView):
    model = Category
    template_name = "app/category.html"
    context_object_name = "eventos_por_categoria"
    
    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Event.objects.filter(category_id=category_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context


    

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user

        # Comentarios
        context["comments"] = event.comments.select_related('user').order_by('-created_at')
        context["errors"] = kwargs.get("errors", {})
        context["is_vendedor"] = user.groups.filter(name="Vendedor").exists() if user.is_authenticated else False

        # Información de calificación
        context["user_has_ticket"] = user.is_authenticated and event.tickets.filter(user=user).exists()
        context["user_rating"] = Rating.objects.filter(user=user, event=event).first() if user.is_authenticated else None
        context["rating_form"] = RatingForm(instance=context["user_rating"]) if user.is_authenticated else None

        # promedio de ratings
        context["average_rating"] = event.ratings.aggregate(Avg("rating"))["rating__avg"] or 0
        context["ratings_count"] = event.ratings.count()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # --- POST de eliminación de rating ---
        rating_id = request.POST.get('delete_rating_id')
        if rating_id:
            rating = get_object_or_404(Rating, pk=rating_id)
            if rating.user == request.user:
                rating.delete()
                messages.success(request, "Reseña eliminada correctamente")
            else:
                messages.error(request, "No puedes eliminar esta reseña")
            return redirect("event_detail", pk=self.object.pk)

        # --- POST de comentario ---
        if "title" in request.POST and "text" in request.POST and "rating" not in request.POST:
            title = request.POST.get("title", "").strip()
            text = request.POST.get("text", "").strip()

            success, errors = Comment.new(
                user=request.user,
                event=self.object,
                title=title,
                text=text
            )

            if success:
                return redirect("event_detail", pk=self.object.pk)

            context = self.get_context_data(errors=errors)
            return self.render_to_response(context)

        # --- POST de rating (nuevo o actualizar) ---
        if "title" in request.POST and "text" in request.POST and "rating" in request.POST:
            user_rating = Rating.objects.filter(user=request.user, event=self.object).first()
            if user_rating:
                form = RatingForm(request.POST, instance=user_rating)
            else:
                form = RatingForm(request.POST)

            if form.is_valid():
                rating = form.save(commit=False)
                rating.user = request.user
                rating.event = self.object
                rating.save()
                return redirect("event_detail", pk=self.object.pk)

            context = self.get_context_data(errors=form.errors)
            context["rating_form"] = form
            return self.render_to_response(context)

        return redirect("event_detail", pk=self.object.pk)

class ProfileView(TemplateView):
    model = User
    template_name = "app/account/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['tickets'] = Ticket.objects.filter(user=self.request.user).order_by("buy_date")
        return context


class RefundRequestView(LoginRequiredMixin, FormView):
    template_name = "app/refund_request.html"
    form_class = RefundRequestForm
    success_url = reverse_lazy('tickets')

    def dispatch(self, request, *args, **kwargs):
        # busco el ticket
        self.ticket = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))

        if RefundRequest.objects.filter(ticket_code=self.ticket.ticket_code, resolved=True).exists():
            messages.error(request, "Ya se ha resuelto una solicitud de reembolso para este ticket.")
            return redirect('tickets')
        
        # verifico si el ticket es del ussuario
        if self.ticket.user != request.user:
            messages.error(request, "No tenés permiso para solicitar reembolso de este ticket.")
            return redirect('tickets')
        
        # segun el enunciado, el evento tiene que haber ocurrido para poder solicitar el reembolso
        if self.ticket.event.date > timezone.now():
            messages.error(request, "El evento aún no ha ocurrido. No se puede solicitar reembolso.")
            return redirect('tickets')
        
        # verifico si ya se solicitó el reembolso
        if RefundRequest.objects.filter(ticket_code=self.ticket.ticket_code, approval_date__isnull=True).exists():
            messages.error(request, "Ya existe una solicitud de reembolso pendiente para este ticket.")
            return redirect('tickets')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        reason = form.cleaned_data.get('reason').strip()
        success, errors = RefundRequest.new(self.request.user, self.ticket.ticket_code, reason)
        
        if not success:
            for error in errors.values():
                form.add_error(None, error)
            return self.form_invalid(form)
        
        messages.success(self.request, "Enviaste la solicitud de reembolso.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.ticket 
        return context
    
class NotificacionLeidaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Notification.objects.filter(users=request.user, is_read=False).update(is_read=True)
        return redirect('notifications')
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "app/comment_confirm_delete.html"
    
    # Redirige al mismo evento después de borrar
    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.event.pk})
    
    def test_func(self):
        # Solo vendedores pueden borrar cualquier comentario
        return self.request.user.groups.filter(name="Vendedor").exists()
    

