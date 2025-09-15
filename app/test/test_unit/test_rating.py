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

        # Crear venue y categoría de prueba
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
            rating=6,
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
        success, rating = Rating.new(
            title="Excelente",
            text="Me encantó",
            rating=5,
            user=self.user,
            event=self.event
        )
        self.assertTrue(success)
        self.assertEqual(rating.title, "Excelente")
        self.assertEqual(rating.text, "Me encantó")
        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.event, self.event)

    def test_new_with_invalid_data(self):
        success, errors = Rating.new(
            title="",
            text="",
            rating=10,
            user=None,
            event=None
        )
        self.assertFalse(success)
        self.assertIn("title", errors)
        self.assertIn("text", errors)
        self.assertIn("rating", errors)
        self.assertIn("user", errors)
        self.assertIn("event", errors)

    # ------------------- Tests de update -------------------
    def test_update_rating_success(self):
        success, rating = Rating.new(
            title="Original",
            text="Texto original",
            rating=3,
            user=self.user,
            event=self.event
        )
        self.assertTrue(success)

        success, updated = rating.update(
            title="Actualizado",
            text="Texto actualizado",
            rating=5,
            user=self.user
        )
        self.assertTrue(success)
        self.assertEqual(updated.title, "Actualizado")
        self.assertEqual(updated.text, "Texto actualizado")
        self.assertEqual(updated.rating, 5)

    def test_update_rating_not_owner(self):
        other_user = User.objects.create_user(
            username="otro",
            email="otro@example.com",
            password="password123"
        )

        success, rating = Rating.new(
            title="Original",
            text="Texto original",
            rating=3,
            user=self.user,
            event=self.event
        )
        self.assertTrue(success)

        success, errors = rating.update(
            title="Hack",
            text="Hackeado",
            rating=1,
            user=other_user
        )
        self.assertFalse(success)
        self.assertIn("user", errors)

    # ------------------- Tests de delete_rating -------------------
    def test_delete_rating_success(self):
        success, rating = Rating.new(
            title="Eliminar",
            text="Texto a eliminar",
            rating=4,
            user=self.user,
            event=self.event
        )
        self.assertTrue(success)
        success, _ = rating.delete_rating(user=self.user)
        self.assertTrue(success)
        self.assertFalse(Rating.objects.filter(pk=rating.pk).exists())

    def test_delete_rating_not_owner(self):
        other_user = User.objects.create_user(
            username="otro",
            email="otro@example.com",
            password="password123"
        )

        success, rating = Rating.new(
            title="No eliminar",
            text="Texto",
            rating=2,
            user=self.user,
            event=self.event
        )
        self.assertTrue(success)
        success, errors = rating.delete_rating(user=other_user)
        self.assertFalse(success)
        self.assertIn("user", errors)
        self.assertTrue(Rating.objects.filter(pk=rating.pk).exists())
