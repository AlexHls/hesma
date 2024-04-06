import zipfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from hesma.rt.models import RTSimulation, RTSimulationLightcurveFile, RTSimulationSpectrumFile
from hesma.rt.views import (
    rt_download_info,
    rt_download_lightcurve,
    rt_download_readme,
    rt_download_spectrum,
    rt_edit,
    rt_landing_view,
    rt_lightcurve_interactive_plot,
    rt_model_view,
    rt_spectrum_interactive_plot,
    rt_upload_lightcurve,
    rt_upload_spectrum,
    rt_upload_view,
)
from hesma.users.models import User


class RTSimulationTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = RTSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )
        self.lightcurve_file = RTSimulationLightcurveFile.objects.create(
            rt_simulation=self.simulation,
            name="Test Lightcurve",
            file=SimpleUploadedFile("test_lightcurve.txt", b"Test lightcurve file contents"),
            date=timezone.now(),
        )
        self.spectrum_file = RTSimulationSpectrumFile.objects.create(
            rt_simulation=self.simulation,
            name="Test Spectrum",
            file=SimpleUploadedFile("test_spectrum.txt", b"Test spectrum file contents"),
            date=timezone.now(),
        )


class RTLandingViewTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_landing_view(self):
        request = self.factory.get(reverse("rt:rt_landing"))
        response = rt_landing_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation")


class RTModelViewTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_model_view(self):
        request = self.factory.get(reverse("rt:detail", args=[self.simulation.id]))
        response = rt_model_view(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation")

    def test_rt_model_view_with_invalid_id(self):
        request = self.factory.get(reverse("rt:detail", args=[100]))
        with self.assertRaises(Http404):
            rt_model_view(request, 100)


class RTUploadViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")

    def test_rt_upload_view_get(self):
        request = self.factory.get(reverse("rt:rt_upload"))
        request.user = self.user
        response = rt_upload_view(request)
        self.assertEqual(response.status_code, 200)

    def test_rt_upload_view_post(self):
        form_data = {
            "name": "Test Simulation",
            "description": "This is a test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        }
        request = self.factory.post(reverse("rt:rt_upload"), data=form_data)
        request.user = self.user
        response = rt_upload_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload successful")


class RTDownloadReadmeTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_download_readme(self):
        request = self.factory.get(reverse("rt:rt_download_readme", args=[self.simulation.id]))
        response = rt_download_readme(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.simulation.readme.name}",
        )


class RTDownloadInfoTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_download_info(self):
        request = self.factory.get(reverse("rt:rt_download_info", args=[self.simulation.id]))
        response = rt_download_info(request, self.simulation.id)
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


class RTEditTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_edit_get(self):
        request = self.factory.get(reverse("rt:rt_edit", args=[self.simulation.id]))
        request.user = self.user
        response = rt_edit(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)

    def test_rt_edit_post(self):
        form_data = {
            "name": "Test Simulation",
            "description": "This is a test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        }
        request = self.factory.post(reverse("rt:rt_edit", args=[self.simulation.id]), data=form_data)
        request.user = self.user
        response = rt_edit(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation")


class RTUploadLightcurveTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_upload_lightcurve_get(self):
        request = self.factory.get(reverse("rt:rt_upload_lightcurve", args=[self.simulation.id]))
        request.user = self.user
        response = rt_upload_lightcurve(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)

    def test_rt_upload_lightcurve_post(self):
        form_data = {
            "name": "Test Lightcurve",
            "description": "This is a test lightcurve",
            "file": SimpleUploadedFile("test_lightcurve.txt", b"Test lightcurve file contents"),
        }
        request = self.factory.post(
            reverse("rt:rt_upload_lightcurve", args=[self.simulation.id]),
            data=form_data,
        )
        request.user = self.user
        response = rt_upload_lightcurve(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload successful")


class RTUploadSpectrumTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_upload_spectrum_get(self):
        request = self.factory.get(reverse("rt:rt_upload_spectrum", args=[self.simulation.id]))
        request.user = self.user
        response = rt_upload_spectrum(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)

    def test_rt_upload_spectrum_post(self):
        form_data = {
            "name": "Test Spectrum",
            "description": "This is a test spectrum",
            "file": SimpleUploadedFile("test_spectrum.txt", b"Test spectrum file contents"),
        }
        request = self.factory.post(reverse("rt:rt_upload_spectrum", args=[self.simulation.id]), data=form_data)
        request.user = self.user
        response = rt_upload_spectrum(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload successful")


class RTLightcurveInteractivePlotTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_lightcurve_interactive_plot(self):
        request = self.factory.get(
            reverse(
                "rt:rt_interactive_lightcurve",
                args=[self.simulation.id, self.lightcurve_file.id],
            )
        )
        response = rt_lightcurve_interactive_plot(request, self.simulation.id, self.lightcurve_file.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Lightcurve")


class RTSpectrumInteractivePlotTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_spectrum_interactive_plot(self):
        request = self.factory.get(
            reverse(
                "rt:rt_interactive_spectrum",
                args=[self.simulation.id, self.spectrum_file.id],
            )
        )
        response = rt_spectrum_interactive_plot(request, self.simulation.id, self.spectrum_file.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Spectrum")


class RTDownloadLightcurveTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_download_lightcurve(self):
        request = self.factory.get(
            reverse(
                "rt:rt_download_lightcurve",
                args=[self.simulation.id, self.lightcurve_file.id],
            )
        )
        response = rt_download_lightcurve(request, self.simulation.id, self.lightcurve_file.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.lightcurve_file.file.name}",
        )


class RTDownloadSpectrumTestCase(RTSimulationTestCase):
    def setUp(self):
        super().setUp()

    def test_rt_download_spectrum(self):
        request = self.factory.get(
            reverse(
                "rt:rt_download_spectrum",
                args=[self.simulation.id, self.spectrum_file.id],
            )
        )
        response = rt_download_spectrum(request, self.simulation.id, self.spectrum_file.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.spectrum_file.file.name}",
        )
