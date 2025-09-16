from app.models import Category, Event, Venue
from app.test.test_e2e.base import BaseE2ETest
from playwright.sync_api import expect
from django.utils import timezone

class HomePageDisplayTest(BaseE2ETest):
    def setUp(self):
        super().setUp()
        
        # Limpiar la DB de pruebas
        Category.objects.all().delete()
        Event.objects.all().delete()
        Venue.objects.all().delete()

        # Crear venue dummy
        self.venue = Venue.objects.create(
            name="Estadio Central",
            address="Calle Falsa 123",
            city="Ushuaia",
            capacity=1000,
            contact="123456"
        )

        # Crear categorías activas
        self.cat_musica = Category.objects.create(
            name="Música",
            description="Eventos musicales",
            is_active=True
        )
        self.cat_arte = Category.objects.create(
            name="Arte",
            description="Exposiciones y más",
            is_active=True
        )

        # Crear evento dummy
        self.event = Event.objects.create(
            title="Concierto de Folklore",
            date=timezone.now().date(),
            venue=self.venue,
            category=self.cat_musica,
            description="Evento de folklore",
            prize=500
        )

    def test_home_page_loads(self):
        # Abrir la página de inicio
        self.page.goto(f"{self.live_server_url}/")

        # ---------------- Carrusel ----------------
        expect(self.page.locator("#carouselExampleFade")).to_have_count(1)

        # ---------------- Logo ----------------
        logo = self.page.get_by_role("link", name="Eventos").first
        expect(logo).to_be_visible()
        expect(logo).to_have_attribute("href", "/")

        # ---------------- Evento principal ----------------
        expect(self.page.get_by_text("Concierto de Folklore")).to_be_visible()

        # ---------------- Categorías ----------------
        expect(self.page.get_by_text("Música")).to_be_visible()
        expect(self.page.get_by_text("Arte")).to_be_visible()

        # ---------------- Botones login/registro ----------------
        expect(self.page.get_by_text("Iniciar Sesión")).to_be_visible()
        expect(self.page.get_by_text("Registrarse")).to_be_visible()
