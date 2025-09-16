from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from app.models import Event, Category, Venue, Comment, Ticket, RefundRequest, Notification, Type_Ticket

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear grupos
        self.admin_group = Group.objects.create(name="Administrador")
        self.vendor_group = Group.objects.create(name="Vendedor")
        self.client_group = Group.objects.create(name="Cliente")

        # Crear usuarios
        self.admin_user = User.objects.create_user(username="admin", password="1234")
        self.vendor_user = User.objects.create_user(username="vendor", password="1234")
        self.client_user = User.objects.create_user(username="client", password="1234")

        # Asignar grupos
        self.admin_user.groups.add(self.admin_group)
        self.vendor_user.groups.add(self.vendor_group)
        self.client_user.groups.add(self.client_group)


        # Crear datos de prueba
        self.venue = Venue.objects.create(
            name="Lugar de prueba",
            address="Calle Falsa 123",
            city="Ushuaia",
            capacity=100,
            contact="Contacto"
        )

        self.category = Category.objects.create(
            name="Categoría de prueba",
            description="Descripción",
            is_active=True
        )

        self.event = Event.objects.create(
            title="Nuevo evento",
            description="Descripción del nuevo evento",
            date=date.today(),
            venue=self.venue,
            category=self.category,
            prize=200)
        
        self.comment = Comment.objects.create(
            user=self.client_user,
            event=self.event,
            title="Comentario válido",
            text="Texto del comentario")
        
        self.ticket = Ticket.objects.create(
            quantity=3,
            type_ticket=Type_Ticket.VIP,
            user=self.client_user,
            event=self.event)
        
        self.refund = RefundRequest.objects.create(
            user=self.client_user,
            ticket_code=self.ticket,
            reason="No puedo asistir")


class DashboardViewTest(BaseTestCase):
    def test_admin_access(self):
        self.client.login(username="admin", password="1234")
        response = self.client.get(reverse("panel_admin:admin_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_vendor_access(self):
        self.client.login(username="vendor", password="1234")
        response = self.client.get(reverse("panel_admin:admin_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_client_access_denied(self):
        self.client.login(username="client", password="1234")
        response = self.client.get(reverse("panel_admin:admin_dashboard"))
        self.assertContains(response, "Este sitio es solo para administradores o vendedores")


class CommentDeleteViewTest(BaseTestCase):
    def test_owner_can_delete(self):
        self.client.login(username="client", password="1234")
        response = self.client.post(reverse("panel_admin:comment_delete", args=[self.comment.id]))
        self.assertEqual(response.status_code, 302) 

    def test_vendor_can_delete_any_comment(self):
        self.client.login(username="vendor", password="1234")
        response = self.client.post(reverse("panel_admin:comment_delete", args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)

    def test_other_client_cannot_delete(self):
        other_client = User.objects.create_user(username="other", password="1234")
        self.client.login(username="other", password="1234")
        response = self.client.post(reverse("panel_admin:comment_delete", args=[self.comment.id]))
        self.assertEqual(response.status_code, 403)

