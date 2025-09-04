from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Event, Venue, Category, Comment
from django.utils import timezone
from datetime import timedelta

class CommentModelTest(TestCase):

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
        errors = Comment.validate(
            user=self.user,
            event=self.event,
            title="Comentario válido",
            text="Texto del comentario"
        )
        self.assertEqual(errors, {})

    def test_validate_with_empty_title(self):
        errors = Comment.validate(
            user=self.user,
            event=self.event,
            title="",
            text="Texto del comentario"
        )
        self.assertIn("title", errors)
        self.assertEqual(errors["title"], "El titulo del comentario es obligatorio")

    def test_validate_with_empty_text(self):
        errors = Comment.validate(
            user=self.user,
            event=self.event,
            title="Comentario válido",
            text=""
        )
        self.assertIn("text", errors)
        self.assertEqual(errors["text"], "El texto del comentario es obligatorio")

    def test_validate_with_no_user(self):
        errors = Comment.validate(
            user=None,
            event=self.event,
            title="Comentario válido",
            text="Texto del comentario"
        )
        self.assertIn("user", errors)
        self.assertEqual(errors["user"], "El usuario del comentario es obligatorio")

    def test_validate_with_no_event(self):
        errors = Comment.validate(
            user=self.user,
            event=None,
            title="Comentario válido",
            text="Texto del comentario"
        )
        self.assertIn("event", errors)
        self.assertEqual(errors["event"], "El evento del comentario es obligatorio")

    # ------------------- Tests de new -------------------

    def test_new_with_valid_data(self):
        success, errors = Comment.new(
            user=self.user,
            event=self.event,
            title="Comentario válido",
            text="Texto del comentario"
        )
        self.assertTrue(success)
        self.assertIsNone(errors)

        comment = Comment.objects.get(title="Comentario válido")
        self.assertEqual(comment.text, "Texto del comentario")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.event, self.event)

    def test_new_with_invalid_data(self):
        success, errors = Comment.new(
            user=None,
            event=None,
            title="",
            text=""
        )
        self.assertFalse(success)
        self.assertIn("user", errors)
        self.assertIn("event", errors)
        self.assertIn("title", errors)
        self.assertIn("text", errors)
