from playwright.sync_api import expect

from app.test.test_e2e.base import BaseE2ETest


# Tests para la página de inicio
class HomePageDisplayTest(BaseE2ETest):
    #Tests relacionados con la visualización de la página de inicio

    def test_home_page_loads(self):
        #Test que verifica que la home carga correctamente
        self.page.goto(f"{self.live_server_url}/")


        # Verificar que el logo este presente
        logo = self.page.get_by_role("link", name="Eventos").first
        expect(logo).to_be_visible()
        expect(logo).to_have_attribute("href", "/")

        # Verificar textos principales de la página
        expect(self.page.locator("#carouselExampleFade")).to_be_visible()
        expect(self.page.get_by_text("Concierto de Folklore")).to_be_visible()

        # Verificar textos de categorias
        expect(self.page.locator("h4", has_text="Categorías")).to_be_visible()
        expect(self.page.get_by_text("No hay categorías disponibles.")).to_be_visible()

        # Verificar botones de login y registro
        expect(self.page.get_by_text("Iniciar Sesión")).to_be_visible()
        expect(self.page.get_by_text("Registrarse")).to_be_visible()
