from smtplib import SMTPException
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from hesma.hydro.models import HydroSimulation
from hesma.pages.models import FAQ, ContactMessage, FAQTopic, News
from hesma.pages.views import contact_view, faq_view, home_view, mymodel_view
from hesma.rt.models import RTSimulation
from hesma.tracer.models import TracerSimulation
from hesma.users.models import User


def add_group(user, group_name):
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)


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

    def test_mymodel_view_not_authenticated(self):
        request = self.factory.get(reverse("pages:mymodels"))
        request.user = AnonymousUser()
        response = mymodel_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Hydro Model")
        self.assertNotContains(response, "Test RT Model")
        self.assertNotContains(response, "Test Tracer Model")
        self.assertContains(response, "You need to be logged in to see your models.")

    def test_mymodel_view_no_user(self):
        request = self.factory.get(reverse("pages:mymodels"))
        request.user = None
        response = mymodel_view(request)
        self.assertEqual(response.status_code, 403)


class UploadSelectorViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@test.com", password="testpass")

    def test_upload_selector_handles_missing_groups(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hydro model")
        self.assertContains(response, "Tracer model")
        self.assertContains(response, "RT model")

    def test_upload_selector_enables_group_links(self):
        add_group(self.user, "hydro_user")
        self.client.force_login(self.user)
        response = self.client.get(reverse("upload"))
        self.assertContains(response, reverse("hydro:hydro_upload"))


class BaseTemplateTestCase(TestCase):
    def test_cookie_consent_script_has_no_malformed_template_tags(self):
        template = (settings.APPS_DIR / "templates" / "base.html").read_text()
        self.assertNotIn("{\n              %", template)
        self.assertNotIn("%\n            }", template)

    def test_base_template_does_not_load_duplicate_bootstrap_modal_scripts(self):
        template = (settings.APPS_DIR / "templates" / "base.html").read_text()
        self.assertNotIn("jquery.bootstrap.modal.forms.js", template)
        self.assertNotIn("bootstrap.bundle.min.js", template)
        self.assertNotIn("bootstrap5.modal.forms.min.js", template)
        self.assertEqual(template.count("bootstrap.min.js"), 1)
        self.assertEqual(template.count("bootstrap5.modal.forms.js"), 1)

    def test_plotly_only_loads_on_interactive_plot_templates(self):
        base_template = (settings.APPS_DIR / "templates" / "base.html").read_text()
        self.assertNotIn("plotly-latest.min.js", base_template)

        plot_templates = [
            settings.APPS_DIR / "templates" / "hydro" / "hydro1d_interactive_plot.html",
            settings.APPS_DIR / "templates" / "rt" / "lightcurve_interactive_plot.html",
            settings.APPS_DIR / "templates" / "rt" / "spectrum_interactive_plot.html",
        ]
        for template_path in plot_templates:
            self.assertIn("plotly-latest.min.js", template_path.read_text())


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.news = [
            {
                "title": "Test News 1",
                "content": "This is test news 1",
                "date": timezone.now(),
            },
            {
                "title": "Test News 2",
                "content": "This is test news 2",
                "date": timezone.now(),
            },
            {
                "title": "Test News 3",
                "content": "This is test news 3",
                "date": timezone.now(),
            },
            {
                "title": "Test News 4",
                "content": "This is test news 4",
                "date": timezone.now(),
            },
            {
                "title": "Test News 5",
                "content": "This is test news 5",
                "date": timezone.now(),
            },
            {
                "title": "Test News 6",
                "content": "This is test news 6",
                "date": timezone.now(),
            },
        ]
        for news in self.news:
            News.objects.create(
                title=news["title"],
                content=news["content"],
                date=news["date"],
            )

    def test_home_view(self):
        request = self.factory.get(reverse("home"))
        response = home_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is test news 1")
        self.assertContains(response, "This is test news 2")
        self.assertContains(response, "This is test news 3")
        self.assertContains(response, "This is test news 4")
        self.assertContains(response, "This is test news 5")
        self.assertNotContains(response, "This is test news 6")


class ContactViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        from captcha.conf import settings as captcha_settings

        captcha_settings.CAPTCHA_TEST_MODE = True

    def valid_post_data(self):
        return {
            "subject": "Test Subject",
            "email": "from@example.com",
            "message": "This is a test message",
            "captcha_0": "TEST",
            "captcha_1": "PASSED",
        }

    def test_contact_view_get(self):
        request = self.factory.get(reverse("pages:contact"))
        response = contact_view(request)
        self.assertEqual(response.status_code, 200)

    def test_contact_view_post(self):
        request = self.factory.post(reverse("pages:contact"), self.valid_post_data())
        with patch("hesma.pages.views.send_contact_email") as send_contact_email:
            response = contact_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank you for contacting us!")
        send_contact_email.assert_called_once()
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_view_post_does_not_save_if_email_fails(self):
        request = self.factory.post(reverse("pages:contact"), self.valid_post_data())
        with patch("hesma.pages.views.send_contact_email", side_effect=SMTPException):
            response = contact_view(request)
        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "Failed to send email", status_code=500)
        self.assertEqual(ContactMessage.objects.count(), 0)
