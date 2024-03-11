from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from hesma.hydro.forms import HydroSimulation1DModelFileForm, HydroSimulationForm
from hesma.meta.models import DOI, Keyword
from hesma.users.models import User


class HydroSimulationFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.doi = DOI.objects.create(
            doi="https://doi.org/10.48550/arXiv.2310.19669",
        )
        self.keyword = Keyword.objects.create(keyword="Test Keyword")

    def test_hydro_simulation_form_valid(self):
        form_data = {
            "name": "Test Simulation",
            "description": "This is a test simulation",
            "user": self.user,
            "DOI": [self.doi],
            "keywords": [self.keyword],
        }
        file_data = {"readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents")}
        form = HydroSimulationForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_hydro_simulation_form_invalid(self):
        form_data = {
            "name": "",
            "description": "This is a test simulation",
            "user": self.user,
        }
        file_data = {"readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents")}
        form = HydroSimulationForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])


class HydroSimulation1DModelFileFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")

    def test_hydro_simulation_1d_model_file_form_valid(self):
        form_data = {
            "name": "Test Model File",
        }
        file_data = {"file": SimpleUploadedFile("test_model_file.txt", b"Test model file contents")}
        form = HydroSimulation1DModelFileForm(data=form_data, files=file_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_hydro_simulation_1d_model_file_form_invalid(self):
        form_data = {
            "name": "Test Model File",
        }
        form = HydroSimulation1DModelFileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["file"], ["This field is required."])
