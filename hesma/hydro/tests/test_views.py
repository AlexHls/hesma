import zipfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from hesma.hydro.models import HydroSimulation
from hesma.hydro.views import (
    hydro_download_info,
    hydro_download_readme,
    hydro_edit,
    hydro_landing_view,
    hydro_model_view,
    hydro_upload_view,
)
from hesma.users.models import User


class HydroLandingViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = HydroSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_hydro_landing_view(self):
        request = self.factory.get(reverse("hydro:hydro_landing"))
        response = hydro_landing_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation")


class HydroModelViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = HydroSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_hydro_model_view(self):
        request = self.factory.get(reverse("hydro:detail", args=[self.simulation.id]))
        response = hydro_model_view(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation")

    def test_hydro_model_view_with_invalid_id(self):
        request = self.factory.get(reverse("hydro:detail", args=[100]))
        with self.assertRaises(Http404):
            hydro_model_view(request, 100)


class HydroUploadViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")

    def test_hydro_upload_view_get(self):
        request = self.factory.get(reverse("hydro:hydro_upload"))
        request.user = self.user
        response = hydro_upload_view(request)
        self.assertEqual(response.status_code, 200)

    def test_hydro_upload_view_post(self):
        form_data = {
            "name": "Test Simulation",
            "description": "This is a test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        }
        request = self.factory.post(reverse("hydro:hydro_upload"), data=form_data)
        request.user = self.user
        response = hydro_upload_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload successful")


class HydroDownloadReadmeTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = HydroSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_hydro_download_readme(self):
        request = self.factory.get(reverse("hydro:hydro_download_readme", args=[self.simulation.id]))
        response = hydro_download_readme(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.simulation.readme.name}",
        )


class HydroDownloadInfoTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = HydroSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_hydro_download_info(self):
        request = self.factory.get(reverse("hydro:hydro_download_info", args=[self.simulation.id]))
        response = hydro_download_info(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.simulation.name}.zip",
        )
        # This is sort of testing the contents twice. The zip generator test
        # already tests the contents of the zip file. This is just to make sure
        # that the response is a valid zip file.
        with zipfile.ZipFile(BytesIO(response.content), "r") as zip_file:
            desired_file = "info.json"
            file_names_in_zip = zip_file.namelist()
            self.assertIn(desired_file, file_names_in_zip)


class HydroEditTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = HydroSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_hydro_edit_get(self):
        request = self.factory.get(reverse("hydro:hydro_edit", args=[self.simulation.id]))
        request.user = self.user
        response = hydro_edit(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)

    def test_hydro_edit_post(self):
        form_data = {
            "name": "Test Simulation Updated",
            "description": "This is an updated test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        }
        request = self.factory.post(reverse("hydro:hydro_edit", args=[self.simulation.id]), data=form_data)
        request.user = self.user
        response = hydro_edit(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation Updated")
