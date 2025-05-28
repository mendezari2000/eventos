import datetime

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from app.models import Event, Venue, Category


class BaseEventTestCase(TestCase):
    """Clase base con la configuración común para todos los tests de eventos"""

    def setUp(self):
        # Crear venue y category de prueba
        self.venue = Venue.objects.create(
            name="Lugar de prueba",
            address="Calle Falsa 123",
            city="Ciudad",
            capacity=100,
            contact="Contacto"
        )

        self.category = Category.objects.create(
            name="Categoría de prueba",
            description="Descripción",
            is_active=True
        )

        # Crear algunos eventos de prueba con venue y category
        self.event1 = Event.objects.create(
            title="Evento 1",
            description="Descripción del evento 1",
            date=timezone.now() + datetime.timedelta(days=1),
            venue=self.venue,
            category=self.category
        )

        self.event2 = Event.objects.create(
            title="Evento 2",
            description="Descripción del evento 2",
            date=timezone.now() + datetime.timedelta(days=2),
            venue=self.venue,
            category=self.category
        )

        # Cliente para hacer peticiones
        self.client = Client()


class EventsListViewTest(BaseEventTestCase):
    """Tests para la vista de listado de eventos"""

    def test_events_view(self):
        """Test que verifica que la vista events funciona correctamente"""
        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/events.html")
        self.assertIn("events", response.context)
        self.assertEqual(len(response.context["events"]), 2)

        # Verificar que los eventos están ordenados por fecha
        events = list(response.context["events"])
        self.assertEqual(events[0].id, self.event1.id)
        self.assertEqual(events[1].id, self.event2.id)


class EventDetailViewTest(BaseEventTestCase):
    """Tests para la vista de detalle de un evento"""

    def test_event_detail_view(self):
        """Test que verifica que la vista event_detail funciona correctamente"""
        response = self.client.get(reverse("event_detail", args=[self.event1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/event_detail.html")
        self.assertIn("event", response.context)
        self.assertEqual(response.context["event"].id, self.event1.id)
