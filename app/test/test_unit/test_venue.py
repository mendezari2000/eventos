from django.test import TestCase
from app.models import Venue


class VenueModelTest(TestCase):
    def setUp(self):
        self.venue = Venue.objects.create(
            name="Sala Central",
            address="Calle Falsa 123",
            city="Ciudad",
            capacity=100,
            contact="contacto@correo.com"
        )
    
    # ------- tests de validate -------
    def test_validate_with_valid_data(self):
        errors = Venue.validate(
            name=self.venue.name,
            address=self.venue.address,
            city=self.venue.city,
            capacity=self.venue.capacity,
            contact=self.venue.contact
        )
        self.assertEqual(errors, {})

    # ------- tests de new -------

    def test_new_with_valid_data(self):
        success, errors = Venue.new(
            name="Auditorio Principal",
            address="Av. Siempre Viva 742",
            city="Springfield",
            capacity=250,
            contact="auditorio@correo.com"
        )
        self.assertTrue(success)
        self.assertIsNone(errors)

        venue = Venue.objects.get(name="Auditorio Principal")

        self.assertEqual(venue.name, "Auditorio Principal")
        self.assertEqual(venue.capacity, 250)    

    def test_new_with_invalid_data(self):
        success, errors = Venue.new(
            name="",
            address="",
            city="",
            capacity=0,
            contact=""
        )
        self.assertFalse(success)
        self.assertIn("name", errors)
        self.assertIn("capacity", errors)

    def test_str_method(self):
        self.assertEqual(str(self.venue), "Sala Central - Ciudad")

    