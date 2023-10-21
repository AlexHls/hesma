import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from hesma.hydro.models import HydroSimulation, HydroSimulationForm
from hesma.users.models import User


class HydroSimulationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = HydroSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_hydro_simulation_str(self):
        self.assertEqual(str(self.simulation), "Test Simulation")

    def test_hydro_simulation_was_published_recently(self):
        self.assertTrue(self.simulation.was_published_recently())

    def test_hydro_simulation_was_published_recently_with_future_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_simulation = HydroSimulation(
            name="Future Simulation",
            description="This is a future simulation",
            user=self.user,
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
            date=time,
        )
        self.assertFalse(future_simulation.was_published_recently())


class HydroSimulationFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")

    def test_hydro_simulation_form_valid(self):
        form_data = {
            "name": "Test Simulation",
            "description": "This is a test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
            "user": self.user,
        }
        form = HydroSimulationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_hydro_simulation_form_invalid(self):
        form_data = {
            "name": "",
            "description": "This is a test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
            "user": self.user,
        }
        form = HydroSimulationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])
