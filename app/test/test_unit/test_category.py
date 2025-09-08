from django.test import TestCase
from app.models import Category

class CategoryModelTest(TestCase):

    def test_validate_with_valid_data(self):
        errors = Category.validate(
            name="Conciertos",
            description="Categoría para eventos musicales"
        )
        self.assertEqual(errors, {})

    def test_validate_with_empty_name(self):
        errors = Category.validate(
            name="",
            description="Descripción válida"
        )
        self.assertIn("name", errors)
        self.assertEqual(errors["name"], "La categoría debe tener un nombre")

    def test_validate_with_empty_description(self):
        errors = Category.validate(
            name="Conciertos",
            description=""
        )
        self.assertIn("description", errors)
        self.assertEqual(errors["description"], "La categoría debe tener una descripción")

    def test_new_with_valid_data(self):
        # Crear categoría con datos válidos
        success, errors = Category.new(
            name="Conciertos",
            description="Categoría para eventos musicales",
            is_active=True
        )
        self.assertTrue(success)
        self.assertIsNone(errors)

        category = Category.objects.get(name="Conciertos")
        self.assertEqual(category.description, "Categoría para eventos musicales")
        self.assertTrue(category.is_active)

    def test_new_with_invalid_data(self):
        #Intentar crear categoría con datos inválidos
        success, errors = Category.new(
            name="",
            description="",
            is_active=False
        )
        self.assertFalse(success)
        self.assertIn("name", errors)
        self.assertIn("description", errors)