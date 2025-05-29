from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from app.models import Event, Venue, Category

class EventModelTest(TestCase):
    def setUp(self):
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

    def test_event_validate_with_valid_data(self):
        date = timezone.now() + timedelta(days=1)
        errors = Event.validate("Título válido", "Descripción válida", date, self.venue, self.category)
        self.assertEqual(errors, {})

    def test_event_validate_with_empty_title(self):
        date = timezone.now() + timedelta(days=1)
        errors = Event.validate("", "Descripción válida", date, self.venue, self.category)
        self.assertIn("title", errors)
        self.assertEqual(errors["title"], "Por favor ingrese un título")

    def test_event_validate_with_empty_description(self):
        date = timezone.now() + timedelta(days=1)
        errors = Event.validate("Título válido", "", date, self.venue, self.category)
        self.assertIn("description", errors)
        self.assertEqual(errors["description"], "Por favor ingrese una descripción")

    def test_event_new_with_valid_data(self):
        date = timezone.now() + timedelta(days=2)
        success, errors = Event.new(
            title="Nuevo evento",
            description="Descripción del nuevo evento",
            date=date,
            venue=self.venue,
            category=self.category
        )

        self.assertTrue(success)
        self.assertIsNone(errors)

        new_event = Event.objects.get(title="Nuevo evento")
        self.assertEqual(new_event.description, "Descripción del nuevo evento")



