from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from app.models import Rating, Event, Venue, Category

class RatingModelTest(TestCase):

    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username="usuario1",
            email="user1@example.com",
            password="password123"
        )

        # Crear venue y categoría de prueba para el evento
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
        errors = Rating.validate(
            title="Buen evento",
            text="Me gustó mucho",
            rating=5,
            user=self.user,
            event=self.event
        )
        self.assertEqual(errors, {})

    def test_validate_with_empty_title(self):
        errors = Rating.validate(
            title="",
            text="Texto",
            rating=4,
            user=self.user,
            event=self.event
        )
        self.assertIn("title", errors)
        self.assertEqual(errors["title"], "Debe ingresar un titulo")

    def test_validate_with_empty_text(self):
        errors = Rating.validate(
            title="Título",
            text="",
            rating=3,
            user=self.user,
            event=self.event
        )
        self.assertIn("text", errors)
        self.assertEqual(errors["text"], "Debe ingresar un texto")

    def test_validate_with_invalid_rating(self):
        errors = Rating.validate(
            title="Título",
            text="Texto",
            rating=6,  # fuera del rango 0-5
            user=self.user,
            event=self.event
        )
        self.assertIn("rating", errors)
        self.assertEqual(errors["rating"], "Debe ingresar un puntuación")

    def test_validate_with_no_user(self):
        errors = Rating.validate(
            title="Título",
            text="Texto",
            rating=4,
            user=None,
            event=self.event
        )
        self.assertIn("user", errors)
        self.assertEqual(errors["user"], "Es obligatorio un usuario")

    def test_validate_with_no_event(self):
        errors = Rating.validate(
            title="Título",
            text="Texto",
            rating=4,
            user=self.user,
            event=None
        )
        self.assertIn("event", errors)
        self.assertEqual(errors["event"], "Es obligatorio ingresar el evento")

    # ------------------- Tests de new -------------------

    def test_new_with_valid_data(self):
        success, errors = Rating.new(
            title="Excelente",
            text="Me encantó",
            rating=5,
            user=self.user,
            event=self.event
        )
        self.assertTrue(success)
        self.assertIsNone(errors)

        rating = Rating.objects.get(title="Excelente")
        self.assertEqual(rating.text, "Me encantó")
        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.event, self.event)

    def test_new_with_invalid_data(self):
        success, errors = Rating.new(
            title="",
            text="",
            rating=10,  # fuera de rango
            user=None,
            event=None
        )
        self.assertFalse(success)
        self.assertIn("title", errors)
        self.assertIn("text", errors)
        self.assertIn("rating", errors)
        self.assertIn("user", errors)
        self.assertIn("event", errors)
