from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from app.models import Category, Event, Venue, Ticket

class CompraExitosaViewTest(TestCase):

    def setUp(self):
        # Crear usuario y loguearlo
        self.user = User.objects.create_user(
            username="usuario1",
            email="user1@example.com",
            password="contrasenia123"
        )
        self.client.login(username="usuario1", password="contrasenia123")

        # Crear venue
        self.venue = Venue.objects.create(
            name="Sala Principal",
            address="Calle Falsa 123",
            city="Ushuaia",
            capacity=100,
            contact="contacto@correo.com"
        )

        # Crear una categoria

        self.category = Category.objects.create(
            name="Musica", 
            description="Eventos musicales", 
            is_active=True)

        # Crear evento
        self.event = Event.objects.create(
            title="Concierto prueba",
            description="Evento de prueba",
            date=timezone.now() + timedelta(days=1),
            venue=self.venue,
            category=self.category,
            prize=100.0
        )

        self.precio_vip = self.event.precio_vip

    def test_crea_ticket_general(self):
        url = reverse('compra_exitosa', args=[self.event.id])
        data = {
            'tipo': 'GENERAL',
            'cantidad': '2'
        }
        response = self.client.post(url, data)
        
        # Redirección correcta
        self.assertEqual(response.status_code, 302)

        # Verificar que el ticket fue creado
        ticket = Ticket.objects.filter(user=self.user, event=self.event).first()
        self.assertIsNotNone(ticket)
        self.assertEqual(Ticket.objects.count(), 1)

        self.assertEqual(ticket.quantity, 2)
        self.assertEqual(ticket.type_ticket, 'GENERAL')
        self.assertEqual(ticket.prize, 100.0)
        self.assertEqual(ticket.total, 200.0)  # 100 * 2

    def test_crea_ticket_vip(self):
        #Prueba que el POST cree un ticket VIP correctamente
        url = reverse('compra_exitosa', args=[self.event.id])
        data = {
            'tipo': 'VIP',
            'cantidad': '1'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.filter(user=self.user, event=self.event).first()
        self.assertIsNotNone(ticket)
        self.assertEqual(Ticket.objects.count(), 1)

        self.assertEqual(ticket.quantity, 1)
        self.assertEqual(ticket.type_ticket, 'VIP')
        self.assertEqual(ticket.prize, self.precio_vip)
        self.assertEqual(ticket.total, self.precio_vip * ticket.quantity)  # 200 * 1

    def test_cantidad_vacia_asigna_1(self):
        # si no se envía cantidad, se asigna 1 por defecto
        url = reverse('compra_exitosa', args=[self.event.id])
        data = {
            'tipo': 'GENERAL',
            'cantidad': ''  
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.filter(user=self.user, event=self.event).first()
        self.assertIsNotNone(ticket)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(ticket.quantity, 1)
