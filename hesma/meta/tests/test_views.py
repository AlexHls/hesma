from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy

from hesma.meta.forms import DOIForm, KeywordForm
from hesma.meta.views import (
    DOICreateViewHydro,
    DOICreateViewRT,
    DOICreateViewTracer,
    KeywordCreateViewHydro,
    KeywordCreateViewRT,
    KeywordCreateViewTracer,
)
from hesma.users.models import User


# The test cases for the DOI Edit views are missing. TODO
class DOICreateViewHydroUploadTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", email="testuser@test.com", password="testpass")

    def test_get(self):
        request = self.factory.get(reverse_lazy("hydro:hydro_upload"))
        request.user = self.user
        response = DOICreateViewHydro.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "meta/create_doi.html")
        self.assertIsInstance(response.context_data["form"], DOIForm)

    def test_post(self):
        data = {
            "doi": "10.5281/zenodo.1234567",
            "author": "Test Author",
            "title": "Test Title",
            "date": "2022-01-01",
        }
        request = self.factory.post(reverse_lazy("hydro:hydro_upload"), data)
        request.user = self.user
        response = DOICreateViewHydro.as_view()(request)
        self.assertEqual(response.status_code, 200)


class DOICreateViewRTUploadTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", email="testuser@test.com", password="testpass")

    def test_get(self):
        request = self.factory.get(reverse_lazy("rt:rt_upload"))
        request.user = self.user
        response = DOICreateViewRT.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "meta/create_doi.html")
        self.assertIsInstance(response.context_data["form"], DOIForm)

    def test_post(self):
        data = {
            "doi": "10.5281/zenodo.1234567",
            "author": "Test Author",
            "title": "Test Title",
            "date": "2022-01-01",
        }
        request = self.factory.post(reverse_lazy("rt:rt_upload"), data)
        request.user = self.user
        response = DOICreateViewRT.as_view()(request)
        self.assertEqual(response.status_code, 200)


class DOICreateViewTracerUploadTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", email="testuser@test.com", password="testpass")

    def test_get(self):
        request = self.factory.get(reverse_lazy("tracer:tracer_upload"))
        request.user = self.user
        response = DOICreateViewTracer.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "meta/create_doi.html")
        self.assertIsInstance(response.context_data["form"], DOIForm)

    def test_post(self):
        data = {
            "doi": "10.5281/zenodo.1234567",
            "author": "Test Author",
            "title": "Test Title",
            "date": "2022-01-01",
        }
        request = self.factory.post(reverse_lazy("tracer:tracer_upload"), data)
        request.user = self.user
        response = DOICreateViewTracer.as_view()(request)
        self.assertEqual(response.status_code, 200)


class KeywordCreateViewHydroTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", email="testuser@test.com", password="testpass")

    def test_get(self):
        request = self.factory.get(reverse_lazy("hydro:hydro_upload"))
        request.user = self.user
        response = KeywordCreateViewHydro.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "meta/create_keyword.html")
        self.assertIsInstance(response.context_data["form"], KeywordForm)

    def test_post(self):
        data = {
            "name": "Test Keyword",
        }
        request = self.factory.post(reverse_lazy("hydro:hydro_upload"), data)
        request.user = self.user
        response = KeywordCreateViewHydro.as_view()(request)
        self.assertEqual(response.status_code, 200)


class KeywordCreateViewRTTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", email="testuser@test.com", password="testpass")

    def test_get(self):
        request = self.factory.get(reverse_lazy("rt:rt_upload"))
        request.user = self.user
        response = KeywordCreateViewRT.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "meta/create_keyword.html")
        self.assertIsInstance(response.context_data["form"], KeywordForm)

    def test_post(self):
        data = {
            "name": "Test Keyword",
        }
        request = self.factory.post(reverse_lazy("rt:rt_upload"), data)
        request.user = self.user
        response = KeywordCreateViewRT.as_view()(request)
        self.assertEqual(response.status_code, 200)


class KeywordCreateViewTracerTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", email="testuser@test.com", password="testpass")

    def test_get(self):
        request = self.factory.get(reverse_lazy("tracer:tracer_upload"))
        request.user = self.user
        response = KeywordCreateViewTracer.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "meta/create_keyword.html")
        self.assertIsInstance(response.context_data["form"], KeywordForm)

    def test_post(self):
        data = {
            "name": "Test Keyword",
        }
        request = self.factory.post(reverse_lazy("tracer:tracer_upload"), data)
        request.user = self.user
        response = KeywordCreateViewTracer.as_view()(request)
        self.assertEqual(response.status_code, 200)
