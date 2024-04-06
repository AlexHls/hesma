from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from hesma.meta.models import DOI, Keyword
from hesma.rt.forms import RTSimulationForm, RTSimulationLightcurveFileForm, RTSimulationSpectrumFileForm
from hesma.users.models import User


class RTSimulationFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.doi = DOI.objects.create(
            doi="https://doi.org/10.48550/arXiv.2310.19669",
        )
        self.keyword = Keyword.objects.create(keyword="Test Keyword")

    def test_rts_simulation_form_valid(self):
        form_data = {
            "name": "Test Simulation",
            "description": "This is a test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
            "user": self.user,
            "DOI": [self.doi],
            "keywords": [self.keyword],
        }
        form = RTSimulationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_rts_simulation_form_invalid(self):
        form_data = {
            "name": "",
            "description": "This is a test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
            "user": self.user,
        }
        form = RTSimulationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])


class RTSimulationLightcurveFileFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")

    def test_rt_simulation_lightcurve_file_form_valid(self):
        form_data = {
            "name": "Test Lightcurve",
        }
        file_data = {"file": SimpleUploadedFile("test_lightcurve.txt", b"Test lightcurve file contents")}
        form = RTSimulationLightcurveFileForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_rt_simulation_lightcurve_file_form_invalid(self):
        form_data = {
            "name": "",
        }
        form = RTSimulationLightcurveFileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["file"], ["This field is required."])


class RTSimulationSpectrumFileFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")

    def test_rt_simulation_spectrum_file_form_valid(self):
        form_data = {
            "name": "Test Spectrum",
        }
        file_data = {"file": SimpleUploadedFile("test_spectrum.txt", b"Test spectrum file contents")}
        form = RTSimulationSpectrumFileForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_rt_simulation_spectrum_file_form_invalid(self):
        form_data = {
            "name": "",
        }
        form = RTSimulationSpectrumFileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["file"], ["This field is required."])
