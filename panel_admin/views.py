from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from app.models import Event, Category, Venue, Comment, Ticket, RefundRequest, Notification

# ------------------- DASHBOARD -------------------
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "panel_admin/dashboard.html"

    def test_func(self):
        user = self.request.user
        return self.request.user.groups.filter(name__in=["Administrador", "Vendedor"]).exists()
    
    def handle_no_permission(self):
        return render(self.request, self.template_name, {'es_admin': False, 'es_vendedor': False})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_groups = self.request.user.groups.values_list('name', flat=True)
        context['es_admin'] = 'Administrador' in user_groups
        context['es_vendedor'] = 'Vendedor' in user_groups
        return context

# ------------------- EVENTOS -------------------
class EventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = "panel_admin/events_list.html"
    context_object_name = 'events'

    def test_func(self):
        return self.request.user.groups.filter(name__in=["Administrador", "Vendedor"]).exists()

    def get_queryset(self):
        user = self.request.user
        return Event.objects.all()  # Admin y vendedor ven todo
        

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    fields = ['title','date','venue','category','description', 'image', 'prize']
    template_name = "panel_admin/event_form.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title','date','venue','category','description', 'image', 'prize']
    template_name = "panel_admin/event_form.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = "panel_admin/event_confirm_delete.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

# ------------------- CATEGORÍAS -------------------
class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = "panel_admin/categories_list.html"
    context_object_name = 'categories'

    def test_func(self):
        return self.request.user.groups.filter(name__in=["Administrador","Vendedor"]).exists()

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    fields = ['name','description','is_active', 'image']
    template_name = "panel_admin/category_form.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name','description','is_active', 'image']
    template_name = "panel_admin/category_form.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = "panel_admin/category_confirm_delete.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

# ------------------- VENUES -------------------
class VenueListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Venue
    template_name = "panel_admin/venues_list.html"
    context_object_name = 'venues'

    def test_func(self):
        return self.request.user.groups.filter(name__in=["Administrador","Vendedor"]).exists()

class VenueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Venue
    fields = ['name','address', 'city', 'capacity', 'contact']
    template_name = "panel_admin/venue_form.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

class VenueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Venue
    fields = ['name','address', 'city', 'capacity', 'contact']
    template_name = "panel_admin/venue_form.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

class VenueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Venue
    template_name = "panel_admin/venue_confirm_delete.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

# ------------------- COMMENTS -------------------
class CommentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Comment
    template_name = 'panel_admin/comments_list.html'
    context_object_name = 'comments'

    def test_func(self):
        # Solo vendedores y administradores
        return self.request.user.groups.filter(name__in=['Administrador', 'Vendedor']).exists()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "panel_admin/comment_confirm_delete.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        user = self.request.user
        comment = self.get_object()
        # Cliente puede eliminar sus propios comentarios, vendedor puede eliminar cualquiera
        return comment.user == user or user.groups.filter(name="Vendedor").exists()

# ------------------- TICKETS -------------------
class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['estado']
    template_name = "panel_admin/ticket_form.html"
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        user = self.request.user
        ticket = self.get_object()
        if user.groups.filter(name="Administrador").exists():
            return True
        elif user.groups.filter(name="Vendedor").exists():
            return ticket.solicitud_reembolso_aceptada
        return False

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    template_name = "panel_admin/ticket_confirm_delete.html"
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return TicketUpdateView.test_func(self)

# ------------------- REFUND REQUEST -------------------
class RefundRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = RefundRequest
    template_name = 'panel_admin/refunds_list.html'
    context_object_name = 'refunds'

    def test_func(self):
        return self.request.user.groups.filter(name='Vendedor').exists()

from django.utils import timezone

class RefundRequestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RefundRequest
    fields = []
    template_name = "panel_admin/refund_request_form.html"
    success_url = reverse_lazy('panel_admin:refunds_list')

    def test_func(self):
        # Solo vendedores pueden procesar solicitudes
        return self.request.user.groups.filter(name="Vendedor").exists()

    def form_valid(self, form):
        refund = form.instance
        decision = self.request.POST.get('decision')

        if decision == 'approve':
            refund.approved = True
            refund.approval_date = timezone.now()
            refund.rejected = False
            refund.resolved = True
            Notification.new(
                title='Solicitud de Reembolso',
                message=f'Tu solicitud de reembolso para el ticket "{refund.ticket_code}" ha sido aprobada.',
                users=[refund.user],
                priority='HIGH',
            )
        elif decision == 'reject':
            refund.approved = False
            refund.rejected = True
            refund.resolved = True
            Notification.new(
                title='Solicitud de Reembolso',
                message=f'Tu solicitud de reembolso para el ticket "{refund.ticket_code}" ha sido rechazada.',
                users=[refund.user],
                priority='HIGH',
            )
        else:
            refund.resolved = False  # Si no se toma ninguna decisión, no se resuelve

        return super().form_valid(form)

# ------------------- NOTIFICATIONS -------------------
class NotificationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Notification
    template_name = "panel_admin/notifications_list.html"
    context_object_name = 'notifications'

    def test_func(self):
        return self.request.user.groups.filter(name__in=["Administrador","Vendedor"]).exists()

class NotificationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Notification
    fields = ['title','message','priority','users']
    template_name = "panel_admin/notification_form.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

class NotificationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Notification
    fields = ['title','message','priority','users']
    template_name = "panel_admin/notification_form.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()

class NotificationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Notification
    template_name = "panel_admin/notification_confirm_delete.html"
    success_url = reverse_lazy('panel_admin:admin_dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name="Administrador").exists()
