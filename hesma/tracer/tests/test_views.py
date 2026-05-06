from django.contrib.auth.models import AnonymousUser, Group
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import content_disposition_header

from hesma.tracer.models import TracerSimulation
from hesma.tracer.views import (
    tracer_download_info,
    tracer_download_readme,
    tracer_edit,
    tracer_landing_view,
    tracer_model_view,
    tracer_upload_view,
)
from hesma.users.models import User


def add_group(user, group_name):
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)


class TracerLandingViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = TracerSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )
        # Set up 10 more simulations
        for i in range(10):
            TracerSimulation.objects.create(
                name=f"Test Simulation {i}",
                description=f"This is a test simulation {i}",
                user=self.user,
                date=timezone.now(),
                readme=SimpleUploadedFile(f"test_readme_{i}.txt", f"Test readme file contents {i}".encode()),
            )

    def test_tracer_landing_view(self):
        request = self.factory.get(reverse("tracer:tracer_landing"))
        response = tracer_landing_view(request)
        self.assertEqual(response.status_code, 200)
        # Check that simulations are first simulation is only displayed once
        # I.e. in the "All simulations" section
        self.assertEqual(response.content.decode().count("Test Simulation 0"), 1)
        # Check that the latest simulations are displayed in the "Latest simulations" section
        # and the "All simulations" section
        self.assertEqual(response.content.decode().count("Test Simulation 9"), 2)


class TracerModelViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = TracerSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_tracer_model_view(self):
        request = self.factory.get(reverse("tracer:detail", args=[self.simulation.id]))
        response = tracer_model_view(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation")

    def test_tracer_model_view_with_invalid_id(self):
        request = self.factory.get(reverse("tracer:detail", args=[100]))
        with self.assertRaises(Http404):
            tracer_model_view(request, 100)


class TracerUploadViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        add_group(self.user, "tracer_user")

    def test_tracer_upload_view_get(self):
        request = self.factory.get(reverse("tracer:tracer_upload"))
        request.user = self.user
        response = tracer_upload_view(request)
        self.assertEqual(response.status_code, 200)

    def test_tracer_upload_view_requires_login(self):
        request = self.factory.get(reverse("tracer:tracer_upload"))
        request.user = AnonymousUser()
        response = tracer_upload_view(request)
        self.assertEqual(response.status_code, 302)

    def test_tracer_upload_view_requires_tracer_group(self):
        request = self.factory.get(reverse("tracer:tracer_upload"))
        request.user = User.objects.create(username="nogroup", email="nogroup@test.com")
        with self.assertRaises(PermissionDenied):
            tracer_upload_view(request)

    def test_tracer_upload_view_post(self):
        form_data = {
            "name": "Test Simulation",
            "description": "This is a test simulation",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        }
        request = self.factory.post(reverse("tracer:tracer_upload"), data=form_data)
        request.user = self.user
        response = tracer_upload_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload successful")


class TracerDownloadReadmeTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = TracerSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_tracer_download_readme(self):
        request = self.factory.get(reverse("tracer:tracer_download_readme", args=[self.simulation.id]))
        response = tracer_download_readme(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            content_disposition_header(as_attachment=True, filename=self.simulation.readme.name),
        )

    def test_tracer_download_readme_missing_file(self):
        simulation = TracerSimulation.objects.create(
            name="No README Simulation",
            description="This simulation has no README",
            user=self.user,
            date=timezone.now(),
        )
        request = self.factory.get(reverse("tracer:tracer_download_readme", args=[simulation.id]))
        with self.assertRaises(Http404):
            tracer_download_readme(request, simulation.id)

    def test_tracer_download_readme_invalid_id(self):
        request = self.factory.get(reverse("tracer:tracer_download_readme", args=[100]))
        with self.assertRaises(Http404):
            tracer_download_readme(request, 100)

    def test_tracer_download_readme_missing_physical_file(self):
        readme_name = self.simulation.readme.name
        self.simulation.readme.storage.delete(readme_name)
        request = self.factory.get(reverse("tracer:tracer_download_readme", args=[self.simulation.id]))
        with self.assertRaises(Http404):
            tracer_download_readme(request, self.simulation.id)


class TracerDownloadInfoTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = TracerSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_tracer_download_info(self):
        request = self.factory.get(reverse("tracer:tracer_download_info", args=[self.simulation.id]))
        response = tracer_download_info(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            content_disposition_header(as_attachment=True, filename=f"{self.simulation.name}.zip"),
        )

    def test_tracer_download_info_skips_missing_readme(self):
        simulation = TracerSimulation.objects.create(
            name="No README Simulation",
            description="This simulation has no README",
            user=self.user,
            date=timezone.now(),
        )
        request = self.factory.get(reverse("tracer:tracer_download_info", args=[simulation.id]))
        response = tracer_download_info(request, simulation.id)
        self.assertEqual(response.status_code, 200)

    def test_tracer_download_info_invalid_id(self):
        request = self.factory.get(reverse("tracer:tracer_download_info", args=[100]))
        with self.assertRaises(Http404):
            tracer_download_info(request, 100)


class TracerEditTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.simulation = TracerSimulation.objects.create(
            name="Test Simulation",
            description="This is a test simulation",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_tracer_edit_get(self):
        request = self.factory.get(reverse("tracer:tracer_edit", args=[self.simulation.id]))
        request.user = self.user
        response = tracer_edit(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)

    def test_tracer_edit_requires_login(self):
        request = self.factory.get(reverse("tracer:tracer_edit", args=[self.simulation.id]))
        request.user = AnonymousUser()
        response = tracer_edit(request, self.simulation.id)
        self.assertEqual(response.status_code, 302)

    def test_tracer_edit_requires_owner(self):
        request = self.factory.get(reverse("tracer:tracer_edit", args=[self.simulation.id]))
        request.user = User.objects.create(username="otheruser", email="otheruser@test.com")
        with self.assertRaises(PermissionDenied):
            tracer_edit(request, self.simulation.id)

    def test_tracer_edit_invalid_id(self):
        request = self.factory.get(reverse("tracer:tracer_edit", args=[100]))
        request.user = self.user
        with self.assertRaises(Http404):
            tracer_edit(request, 100)

    def test_tracer_edit_post(self):
        form_data = {
            "name": "Test Simulation Edited",
            "description": "This is a test simulation edited",
            "readme": SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        }
        request = self.factory.post(reverse("tracer:tracer_edit", args=[self.simulation.id]), data=form_data)
        request.user = self.user
        response = tracer_edit(request, self.simulation.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Simulation Edited")
