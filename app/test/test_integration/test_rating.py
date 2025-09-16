from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from app.models import Event, Venue, Category, Ticket, Rating

class RatingIntegrationTest(TestCase):

    def setUp(self):
        # Usuario normal
        self.user = User.objects.create_user(
            username="usuario1",
            email="user1@example.com",
            password="password123"
        )

        # Otro usuario
        self.other_user = User.objects.create_user(
            username="otro",
            email="otro@example.com",
            password="password123"
        )

        # Venue, categoría y evento
        self.venue = Venue.objects.create(
            name="Sala Principal",
            address="Calle Falsa 123",
            city="Ciudad",
            capacity=100,
            contact="contacto@correo.com"
        )

        self.category = Category.objects.create(
            name="Musica",
            description="Eventos musicales",
            is_active=True
        )

        self.event = Event.objects.create(
            title="Concierto prueba",
            description="Evento de prueba",
            date=timezone.now() + timedelta(days=1),
            venue=self.venue,
            category=self.category,
            prize=100
        )

        # Darle ticket al usuario para poder calificar
        self.ticket = Ticket.objects.create(
            user=self.user,
            event=self.event,
            quantity=1,
            prize=self.event.prize,
            total=self.event.prize
        )

        self.url = reverse("event_detail", args=[self.event.id])

    def test_create_valid_rating(self):
        self.client.login(username="usuario1", password="password123")
        data = {"form_type": "rating", "title": "Excelente", "text": "Me encantó", "rating": 5}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirige al detalle
        self.assertTrue(Rating.objects.filter(user=self.user, event=self.event, title="Excelente").exists())

    def test_create_invalid_rating(self):
        self.client.login(username="usuario1", password="password123")
        data = {"form_type": "rating", "title": "", "text": "", "rating": 10}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Devuelve el template con errores
        self.assertContains(response, "Este campo es obligatorio.")
        self.assertContains(response, "Este campo es obligatorio.")
        self.assertContains(response, "Este campo es obligatorio.")
        self.assertEqual(Rating.objects.filter(user=self.user, event=self.event).count(), 0)

    def test_update_rating(self):
        # Crear rating inicial
        rating = Rating.objects.create(title="Original", text="Texto original", rating=3, user=self.user, event=self.event)
        self.client.login(username="usuario1", password="password123")
        data = {"form_type": "rating", "title": "Actualizado", "text": "Nuevo texto", "rating": 5}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        rating.refresh_from_db()
        self.assertEqual(rating.title, "Actualizado")
        self.assertEqual(rating.text, "Nuevo texto")
        self.assertEqual(rating.rating, 5)

    def test_owner_delete_rating(self):
        rating = Rating.objects.create(title="Eliminar", text="Texto a eliminar", rating=4, user=self.user, event=self.event)
        self.client.login(username="usuario1", password="password123")
        data = {"delete_rating_id": rating.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Rating.objects.filter(pk=rating.id).exists())

    def test_delete_other_user(self):
        rating = Rating.objects.create(title="No eliminar", text="Texto", rating=2, user=self.user, event=self.event)
        self.client.login(username="otro", password="password123")
        data = {"delete_rating_id": rating.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Rating.objects.filter(pk=rating.id).exists())