import zipfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from hesma.hydro.models import HydroSimulation, HydroSimulation1DModelFile
from hesma.hydro.views import (
    hydro_download_hydro1d,
    hydro_download_info,
    hydro_download_readme,
    hydro_edit,
    hydro_hydro1d_interactive_plot,
    hydro_landing_view,
    hydro_model_view,
    hydro_upload_hydro1d,
    hydro_upload_view,
)
from hesma.users.models import User


class HydroViewsTestCase(TestCase):
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
        self.hydro1d_file = HydroSimulation1DModelFile.objects.create(
            hydro_simulation=self.simulation,
            name="Test Hydro1D File",
            file=SimpleUploadedFile("test_hydro1d_file.json", b"Test hydro1d file contents"),
            date=timezone.now(),
        )


class HydroLandingViewTestCase(HydroViewsTestCase):
    def setUp(self):
        super().setUp()
        # Set up 10 more simulations
        for i in range(10):
            HydroSimulation.objects.create(
                name=f"Test Simulation {i}",
                description=f"This is a test simulation {i}",
                user=self.user,
                date=timezone.now(),
                readme=SimpleUploadedFile(f"test_readme_{i}.txt", f"Test readme file contents {i}".encode()),
            )

    def test_hydro_landing_view(self):
        request = self.factory.get(reverse("hydro:hydro_landing"))
        response = hydro_landing_view(request)
        self.assertEqual(response.status_code, 200)
        # Check that simulations are first simulation is only displayed once
        # I.e. in the "All simulations" section
        self.assertEqual(response.content.decode().count("Test Simulation 0"), 1)
        # Check that the latest simulations are displayed in the "Latest simulations" section
        # and the "All simulations" section
        self.assertEqual(response.content.decode().count("Test Simulation 9"), 2)


class HydroModelViewTestCase(HydroViewsTestCase):
    def setUp(self):
        super().setUp()

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
        request = self.factory.post(
            reverse("hydro:hydro_upload"),
            data=form_data,
        )
        request.user = self.user
        response = hydro_upload_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload successful")


class HydroDownloadReadmeTestCase(HydroViewsTestCase):
    def setUp(self):
        super().setUp()

    def test_hydro_download_readme(self):
        request = self.factory.get(reverse("hydro:hydro_download_readme", args=[self.simulation.id]))
        response = hydro_download_readme(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.simulation.readme.name}",
        )


class HydroDownloadInfoTestCase(HydroViewsTestCase):
    def setUp(self):
        super().setUp()

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


class HydroEditTestCase(HydroViewsTestCase):
    def setUp(self):
        super().setUp()

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
        request = self.factory.post(
            reverse("hydro:hydro_edit", args=[self.simulation.id]),
            data=form_data,
        )
        request.user = self.user
        response = hydro_edit(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation Updated")


class HydroUploadHydro1DTestCase(HydroViewsTestCase):
    def setUp(self):
        super().setUp()

    def test_hydro_upload_hydro1d_view_get(self):
        request = self.factory.get(reverse("hydro:hydro_upload_hydro1d", args=[self.simulation.id]))
        request.user = self.user
        response = hydro_upload_hydro1d(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)

    def test_hydro_upload_hydro1d_view_post(self):
        form_data = {
            "name": "Test Simulation",
            "description": "This is a test simulation",
            "file": SimpleUploadedFile("test_hydro1d_file.json", b"Test hydro1d file contents"),
        }
        request = self.factory.post(
            reverse("hydro:hydro_upload_hydro1d", args=[self.simulation.id]),
            data=form_data,
        )
        request.user = self.user
        response = hydro_upload_hydro1d(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload successful")


class HydroHydro1DInteractivePlotTestCase(HydroViewsTestCase):
    def setUp(self):
        super().setUp()

    def test_hydro_hydro1d_interactive_plot(self):
        request = self.factory.get(
            reverse(
                "hydro:hydro_interactive_hydro1d",
                args=[self.simulation.id, self.hydro1d_file.id],
            )
        )
        response = hydro_hydro1d_interactive_plot(request, self.simulation.id, self.hydro1d_file.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation")


class HydroDownloadHydro1DTestCase(HydroViewsTestCase):
    def setUp(self):
        super().setUp()

    def test_hydro_download_hydro1d(self):
        request = self.factory.get(
            reverse(
                "hydro:hydro_download_hydro1d",
                args=[self.simulation.id, self.hydro1d_file.id],
            )
        )
        response = hydro_download_hydro1d(request, self.simulation.id, self.hydro1d_file.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.hydro1d_file.file.name}",
        )
