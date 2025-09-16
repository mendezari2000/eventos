from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta
from app.models import Event, Venue, Category, Comment


class EventDetailViewTest(TestCase):
    def setUp(self):
        # usuario normal
        self.user = User.objects.create_user(
            username="usuario1",
            email="user1@example.com",
            password="contrasenia123"
        )
        # usuario vendedor
        self.vendedor = User.objects.create_user(
            username="vendedor1",
            email="vendedor@example.com",
            password="contrasenia123"
        )
        group = Group.objects.create(name="Vendedor")
        self.vendedor.groups.add(group)

        # datos
        self.venue = Venue.objects.create(
            name="Sala Principal",
            address="Calle Falsa 123",
            city="Ushuaia",
            capacity=100,
            contact="contacto@correo.com"
        )
        self.category = Category.objects.create(
            name="Musica", description="Eventos musicales", is_active=True
        )
        self.event = Event.objects.create(
            title="Concierto prueba",
            description="Evento de prueba",
            date=timezone.now() + timedelta(days=1),
            venue=self.venue,
            category=self.category,
            prize=100.0
        )
        self.url = reverse("event_detail", args=[self.event.id])

    def test_get_event_detail_view_funciona(self):

        # Devuelve 200 y usa el template correcto

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/event_detail.html")
        self.assertEqual(response.context["event"], self.event)

    def test_muestra_comentarios(self):
        comment = Comment.objects.create(
            user=self.user,
            event=self.event,
            title="Gran show",
            text="Me encantó!"
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Gran show")
        self.assertContains(response, "Me encantó!")

    def test_crea_comentario_valido(self):
        
        self.client.login(username="usuario1", password="contrasenia123")
        data = {
            "form_type": "comment",
            "title": "Nuevo comentario",
            "text": "Texto de prueba"
        }
        response = self.client.post(self.url, data)

        # Redirige al detalle
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(user=self.user, event=self.event, title="Nuevo comentario").exists()
        )

    def test_comentario_invalido(self):
        
        self.client.login(username="usuario1", password="contrasenia123")
        data = {
            "form_type": "comment",
            "title": "",
            "text": ""
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "El titulo del comentario es obligatorio") 
        self.assertContains(response, "El texto del comentario es obligatorio")
        self.assertEqual(Comment.objects.count(), 0)

    def test_context_incluye_vendedor(self):
        
        self.client.login(username="vendedor1", password="contrasenia123")
        response = self.client.get(self.url)
        self.assertTrue(response.context["is_vendedor"])