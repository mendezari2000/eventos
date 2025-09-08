from django.test import TestCase
from django.utils.timezone import now
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
        date = now() + timedelta(days=1)
        errors = Event.validate("Título válido", "Descripción válida", date, self.venue, self.category, prize=100)
        self.assertEqual(errors, {})

    def test_event_validate_with_empty_title(self):
        date = now() + timedelta(days=1)
        errors = Event.validate("", "Descripción válida", date, self.venue, self.category)
        self.assertIn("title", errors)

    def test_event_validate_with_empty_description(self):
        date = now() + timedelta(days=1)
        errors = Event.validate("Título válido", "", date, self.venue, self.category)
        self.assertIn("description", errors)

    def test_event_validate_with_past_date(self):
        date = now() - timedelta(days=1)
        errors = Event.validate("Título", "Descripción", date, self.venue, self.category)
        self.assertIn("date", errors)

    def test_event_validate_with_null_venue(self):
        date = now() + timedelta(days=1)
        errors = Event.validate("Título", "Descripción", date, None, self.category)
        self.assertIn("venue", errors)

    def test_event_validate_with_null_category(self):
        date = now() + timedelta(days=1)
        errors = Event.validate("Título", "Descripción", date, self.venue, None)
        self.assertIn("category", errors)

    def test_event_validate_with_negative_prize(self):
        date = now() + timedelta(days=1)
        errors = Event.validate("Título", "Descripción", date, self.venue, self.category, prize=-50)
        self.assertIn("prize", errors)

    def test_event_new_with_valid_data(self):
        date = now() + timedelta(days=2)
        success, errors = Event.new(
            title="Nuevo evento",
            description="Descripción del nuevo evento",
            date=date,
            venue=self.venue,
            category=self.category,
            prize=200
        )

        self.assertTrue(success)
        self.assertIsNone(errors)

        new_event = Event.objects.get(title="Nuevo evento")
        self.assertEqual(new_event.prize, 200)

    def test_event_precio_vip_property(self):
        event = Event.objects.create(
            title="Evento VIP",
            description="Desc",
            date=now() + timedelta(days=1),
            venue=self.venue,
            category=self.category,
            prize=150
        )
        self.assertEqual(event.precio_vip, 300)

    def test_event_update_method(self):
        event = Event.objects.create(
            title="Viejo título",
            description="Vieja descripción",
            date=now() + timedelta(days=1),
            venue=self.venue,
            category=self.category,
            prize=100
        )

        new_date = now() + timedelta(days=5)
        event.update(
            title="Nuevo título",
            description="Nueva descripción",
            date=new_date,
            prize=250
        )

        updated_event = Event.objects.get(id=event.id)
        self.assertEqual(updated_event.title, "Nuevo título")
        self.assertEqual(updated_event.description, "Nueva descripción")
        self.assertEqual(updated_event.date, new_date)
        self.assertEqual(updated_event.prize, 250)
