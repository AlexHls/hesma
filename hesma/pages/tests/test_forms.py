from django.test import TestCase

from hesma.pages.forms import ContactMessageForm


class ContactMessageFormTestCase(TestCase):
    def setUp(self):
        from captcha.conf import settings as captcha_settings

        captcha_settings.CAPTCHA_TEST_MODE = True

    def test_contact_message_form_valid(self):
        form_data = {
            "subject": "Test Subject",
            "email": "from@example.com",
            "message": "This is a test message",
            "captcha_0": "TEST",
            "captcha_1": "PASSED",
        }
        form = ContactMessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_message_form_invalid_captcha(self):
        form_data = {
            "subject": "Test Subject",
            "email": "from@example.com",
            "message": "This is a test message",
            "captcha_0": "TEST",
            "captcha_1": "FAILED",
        }
        form = ContactMessageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_contact_message_form_invalid_email(self):
        form_data = {
            "subject": "Test Subject",
            "email": "fromexample.com",
            "message": "This is a test message",
            "captcha_0": "TEST",
            "captcha_1": "PASSED",
        }
        form = ContactMessageForm(data=form_data)
        self.assertFalse(form.is_valid())
