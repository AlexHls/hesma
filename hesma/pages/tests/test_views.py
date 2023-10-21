from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from hesma.hydro.models import HydroSimulation
from hesma.pages.models import FAQ, FAQTopic
from hesma.pages.views import faq_view, mymodel_view
from hesma.rt.models import RTSimulation
from hesma.tracer.models import TracerSimulation
from hesma.users.models import User


class FAQViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.topic = FAQTopic.objects.create(
            name="Test Topic",
            description="This is a test topic",
            order=1,
        )
        self.faq = FAQ.objects.create(
            topic=self.topic,
            question="Test Question",
            answer="Test Answer",
            order=1,
        )

    def test_faq_view(self):
        request = self.factory.get(reverse("pages:faq"))
        response = faq_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Topic")
        self.assertContains(response, "Test Question")


class MyModelViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")
        self.hydro_model = HydroSimulation.objects.create(
            name="Test Hydro Model",
            description="This is a test hydro model",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )
        self.rt_model = RTSimulation.objects.create(
            name="Test RT Model",
            description="This is a test RT model",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )
        self.tracer_model = TracerSimulation.objects.create(
            name="Test Tracer Model",
            description="This is a test tracer model",
            user=self.user,
            date=timezone.now(),
            readme=SimpleUploadedFile("test_readme.txt", b"Test readme file contents"),
        )

    def test_mymodel_view(self):
        request = self.factory.get(reverse("pages:mymodels"))
        request.user = self.user
        response = mymodel_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Hydro Model")
        self.assertContains(response, "Test RT Model")
        self.assertContains(response, "Test Tracer Model")
