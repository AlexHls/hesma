from django.test import TestCase
from django.utils import timezone

from hesma.pages.models import ContactMessage


class MailingTestCase(TestCase):
    def setUp(self):
        self.contact = ContactMessage.objects.create(
            subject="Test Subject",
            email="from@example.com",
            message="This is a test message",
            date=timezone.now(),
        )

    def test_send_contact_email(self):
        # TODO Implement this test. Right now I have no idea how to test this.
        pass
