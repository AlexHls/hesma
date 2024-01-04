from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from hesma.meta.models import DOI
from hesma.rt.forms import RTSimulationForm
from hesma.users.models import User


class RTSimulationFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.doi = DOI.objects.create(
            doi="https://doi.org/10.48550/arXiv.2310.19669",
        )

    def test_rts_simulation_form_valid(self):
        form_data = {
            "name": "Test Simulation",
            "description": "This is a test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
            "user": self.user,
            "DOI": [self.doi],
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
