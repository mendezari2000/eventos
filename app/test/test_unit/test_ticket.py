from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from app.models import Ticket, Event, Venue, Category, Type_Ticket

class TicketModelTest(TestCase):

    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username="usuario1",
            email="user1@example.com",
            password="password123"
        )

        # Crear venue y categoría de prueba
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

        # Crear evento de prueba
        self.event = Event.objects.create(
            title="Evento 1",
            description="Descripción del evento 1",
            date=timezone.now() + timedelta(days=1),
            venue=self.venue,
            category=self.category
        )

    # ------------------- Tests de validate -------------------

    def test_validate_with_valid_data(self):
        errors = Ticket.validate(
            quantity=2,
            type_ticket=Type_Ticket.GENERAL,
            user=self.user,
            event=self.event
        )
        self.assertEqual(errors, {})

    def test_validate_with_negative_quantity(self):
        errors = Ticket.validate(
            quantity=-1,
            type_ticket=Type_Ticket.GENERAL,
            user=self.user,
            event=self.event
        )
        self.assertIn("quantity", errors)
        self.assertEqual(errors["quantity"], "Debe ingresar una cantidad valida")

    def test_validate_with_invalid_type_ticket(self):
        errors = Ticket.validate(
            quantity=1,
            type_ticket="premium",  # no existe
            user=self.user,
            event=self.event
        )
        self.assertIn("type_ticket", errors)
        self.assertEqual(errors["type_ticket"], "Debe ingresar un tipo de ticket valido")

    def test_validate_with_no_user(self):
        errors = Ticket.validate(
            quantity=1,
            type_ticket=Type_Ticket.GENERAL,
            user=None,
            event=self.event
        )
        self.assertIn("user", errors)
        self.assertEqual(errors["user"], "Debe asignarle el ticket a un usuario")

    def test_validate_with_no_event(self):
        errors = Ticket.validate(
            quantity=1,
            type_ticket=Type_Ticket.GENERAL,
            user=self.user,
            event=None
        )
        self.assertIn("event", errors)
        self.assertEqual(errors["event"], "Debe asignarle el ticket a un evento")

    # ------------------- Tests de new -------------------

    def test_new_with_valid_data(self):
        success, errors = Ticket.new(
            quantity=3,
            type_ticket=Type_Ticket.VIP,
            user=self.user,
            event=self.event
        )
        self.assertTrue(success)
        self.assertIsNone(errors)

        ticket = Ticket.objects.get(user=self.user, event=self.event)
        self.assertEqual(ticket.quantity, 3)
        self.assertEqual(ticket.type_ticket, Type_Ticket.VIP)
        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.event, self.event)

    def test_new_with_invalid_data(self):
        success, errors = Ticket.new(
            quantity=-5,
            type_ticket="premium",
            user=None,
            event=None
        )
        self.assertFalse(success)
        self.assertIn("quantity", errors)
        self.assertIn("type_ticket", errors)
        self.assertIn("user", errors)
        self.assertIn("event", errors)
