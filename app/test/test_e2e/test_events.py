import datetime

from django.utils import timezone
from playwright.sync_api import expect

from app.models import Event, Venue, Category

from app.test.test_e2e.base import BaseE2ETest


class EventBaseTest(BaseE2ETest):
    #Clase base específica para tests de eventos

    def setUp(self):
        super().setUp()

        # Crear dependencias
        self.venue = Venue.objects.create(
            name="Salón Principal",
            address="Calle Falsa 123",
            city="Ciudad Test",
            capacity=100,
            contact="contacto@example.com",
        )
        self.category = Category.objects.create(
            name="Conferencia",
            description="Conferencias y charlas técnicas",
            is_active=True,
        )

        # Evento 1
        event_date1 = timezone.make_aware(datetime.datetime(2025, 2, 10, 10, 10))
        self.event1 = Event.objects.create(
            title="Evento de prueba 1",
            description="Descripción del evento 1",
            date=event_date1,
            venue=self.venue,
            category=self.category,
        )

        # Evento 2
        event_date2 = timezone.make_aware(datetime.datetime(2025, 3, 15, 14, 30))
        self.event2 = Event.objects.create(
            title="Evento de prueba 2",
            description="Descripción del evento 2",
            date=event_date2,
            venue=self.venue,
            category=self.category,
        )


    def _cards_have_event_info(self):
        #Verifica que las tarjetas tienen la información correcta de eventos
        cards = self.page.locator(".event-card")
        expect(cards).to_have_count(2)

        # Verificar datos del primer evento
        card0 = cards.nth(0)
        expect(card0.locator(".card-title")).to_have_text("Evento de prueba 1")
        expect(card0.locator(".card-body")).to_contain_text("10/02/2025 10:10")
        expect(card0.locator(".card-body")).to_contain_text("Salón Principal")

        # Verificar datos del segundo evento
        card1 = cards.nth(1)
        expect(card1.locator(".card-title")).to_have_text("Evento de prueba 2")
        expect(card1.locator(".card-body")).to_contain_text("15/03/2025 14:30")
        expect(card1.locator(".card-body")).to_contain_text("Salón Principal")    

    def _cards_have_correct_actions(self):
        #Verifica que las acciones en las tarjetas sean correctas
        card0 = self.page.locator(".event-card").nth(0)

        # Botón de comprar visible
        buy_button = card0.get_by_role("link", name="Comprar")
        expect(buy_button).to_be_visible()
        expect(buy_button).to_have_attribute("href", f"/events/{self.event1.id}/")


class EventDisplayTest(EventBaseTest):
    #Tests relacionados con la visualización de la página de eventos

    def test_events_page_display(self):
        self.page.goto(f"{self.live_server_url}/events/")

        expect(self.page).to_have_title("Eventos")

        cards = self.page.locator(".event-card")
        expect(cards).to_have_count(2)

        self._cards_have_event_info()
        self._cards_have_correct_actions()

    def test_events_page_no_events(self):
        #Test que verifica el comportamiento cuando no hay eventos
        # Eliminar todos los eventos
        Event.objects.all().delete()

        # Ir a la página de eventos
        self.page.goto(f"{self.live_server_url}/events/")

        # Verificar que existe un mensaje indicando que no hay eventos
        no_events_message = self.page.locator("text=No hay eventos disponibles")
        expect(no_events_message).to_be_visible()
