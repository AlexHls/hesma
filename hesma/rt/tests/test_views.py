from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from hesma.rt.models import RTSimulation
from hesma.rt.views import (
    rt_download_info,
    rt_download_readme,
    rt_edit,
    rt_landing_view,
    rt_model_view,
    rt_upload_view,
)
from hesma.users.models import User


class RTLandingViewTestCase(TestCase):
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

    def test_rt_landing_view(self):
        request = self.factory.get(reverse("rt:rt_landing"))
        response = rt_landing_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation")


class RTModelViewTestCase(TestCase):
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


class RTDownloadReadmeTestCase(TestCase):
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

    def test_rt_download_readme(self):
        request = self.factory.get(reverse("rt:rt_download_readme", args=[self.simulation.id]))
        response = rt_download_readme(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.simulation.readme.name}",
        )


class RTDownloadInfoTestCase(TestCase):
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

    def test_rt_download_info(self):
        request = self.factory.get(reverse("rt:rt_download_info", args=[self.simulation.id]))
        response = rt_download_info(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.simulation.name}.zip",
        )


class RTEditTestCase(TestCase):
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
