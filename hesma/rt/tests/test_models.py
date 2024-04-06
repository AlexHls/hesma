import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from hesma.meta.models import DOI, Keyword
from hesma.rt.models import RTSimulation, RTSimulationLightcurveFile, RTSimulationSpectrumFile
from hesma.users.models import User


class RTSimulationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.doi = DOI.objects.create(
            doi="https://doi.org/10.48550/arXiv.2310.19669",
        )
        self.keyword = Keyword.objects.create(keyword="Test Keyword")
        self.simulation = RTSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )
        self.simulation.DOI.add(self.doi)
        self.simulation.keywords.add(self.keyword)

    def test_rts_simulation_str(self):
        self.assertEqual(str(self.simulation), "Test Simulation")

    def test_rts_simulation_was_published_recently(self):
        self.assertTrue(self.simulation.was_published_recently())

    def test_rts_simulation_was_published_recently_with_future_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_simulation = RTSimulation(
            name="Future Simulation",
            description="This is a future simulation",
            user=self.user,
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
            date=time,
        )
        self.assertFalse(future_simulation.was_published_recently())


class RTSimulationLightcurveFileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = RTSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )
        self.model_file = RTSimulationLightcurveFile.objects.create(
            rt_simulation=self.simulation,
            name="Test Lightcurve",
            file=SimpleUploadedFile("test_lightcurve.txt", b"Test lightcurve file contents"),
            date=timezone.now(),
            description="This is a test lightcurve file",
            is_valid_hesma_file=False,
            thumbnail=SimpleUploadedFile("test_thumbnail.png", b"Test thumbnail file contents"),
        )

    def test_rt_simulation_lightcurve_file_str(self):
        self.assertEqual(str(self.model_file), "Test Lightcurve")

    def test_rt_simulation_lightcurve_file_was_published_recently(self):
        self.assertTrue(self.model_file.was_published_recently())

    def test_rt_simulation_lightcurve_file_was_published_recently_with_future_date(
        self,
    ):
        time = timezone.now() + datetime.timedelta(days=30)
        future_model_file = RTSimulationLightcurveFile(
            rt_simulation=self.simulation,
            name="Future Lightcurve",
            file=SimpleUploadedFile("test_lightcurve.txt", b"Test lightcurve file contents"),
            date=time,
            description="This is a future lightcurve file",
            is_valid_hesma_file=False,
            thumbnail=SimpleUploadedFile("test_thumbnail.png", b"Test thumbnail file contents"),
        )
        self.assertFalse(future_model_file.was_published_recently())

    def test_rt_simulation_lightcurve_file_get_plot_json(self):
        self.assertEqual(self.model_file.get_plot_json(), None)

    def test_rt_simulation_lightcurve_file_check_if_valid_hesma_file(self):
        self.assertFalse(self.model_file.check_if_valid_hesma_file())


class RTSimulationSpectrumFileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = RTSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )
        self.model_file = RTSimulationSpectrumFile.objects.create(
            rt_simulation=self.simulation,
            name="Test Spectrum",
            file=SimpleUploadedFile("test_spectrum.txt", b"Test spectrum file contents"),
            date=timezone.now(),
            description="This is a test spectrum file",
            is_valid_hesma_file=False,
            thumbnail=SimpleUploadedFile("test_thumbnail.png", b"Test thumbnail file contents"),
        )

    def test_rt_simulation_spectrum_file_str(self):
        self.assertEqual(str(self.model_file), "Test Spectrum")

    def test_rt_simulation_spectrum_file_was_published_recently(self):
        self.assertTrue(self.model_file.was_published_recently())

    def test_rt_simulation_spectrum_file_was_published_recently_with_future_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_model_file = RTSimulationSpectrumFile(
            rt_simulation=self.simulation,
            name="Future Spectrum",
            file=SimpleUploadedFile("test_spectrum.txt", b"Test spectrum file contents"),
            date=time,
            description="This is a future spectrum file",
            is_valid_hesma_file=False,
            thumbnail=SimpleUploadedFile("test_thumbnail.png", b"Test thumbnail file contents"),
        )
        self.assertFalse(future_model_file.was_published_recently())

    def test_rt_simulation_spectrum_file_get_plot_json(self):
        self.assertEqual(self.model_file.get_plot_json(), None)

    def test_rt_simulation_spectrum_file_check_if_valid_hesma_file(self):
        self.assertFalse(self.model_file.check_if_valid_hesma_file())
