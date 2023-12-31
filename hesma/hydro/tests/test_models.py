import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from hesma.hydro.models import HydroSimulation
from hesma.meta.models import DOI, Keyword
from hesma.users.models import User


class HydroSimulationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.doi = DOI.objects.create(
            doi="https://doi.org/10.48550/arXiv.2310.19669",
        )
        self.keyword = Keyword.objects.create(keyword="Test Keyword")
        self.simulation = HydroSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )
        self.simulation.DOI.add(self.doi)
        self.simulation.keywords.add(self.keyword)

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
