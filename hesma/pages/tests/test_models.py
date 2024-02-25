import datetime

from django.test import TestCase
from django.utils import timezone

from hesma.pages.models import FAQ, ContactMessage, FAQTopic, News


class FAQTopicModelTestCase(TestCase):
    def setUp(self):
        self.topic = FAQTopic.objects.create(
            name="Test Topic",
            description="This is a test topic",
            order=1,
        )

    def test_faq_topic_str(self):
        self.assertEqual(str(self.topic), "Test Topic")


class FAQModelTestCase(TestCase):
    def setUp(self):
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

    def test_faq_str(self):
        self.assertEqual(str(self.faq), "Test Question")

    def test_faq_topic_cascade_delete(self):
        self.topic.delete()
        with self.assertRaises(FAQ.DoesNotExist):
            FAQ.objects.get(pk=self.faq.pk)


class NewsModelTestCase(TestCase):
    def setUp(self):
        self.news = News.objects.create(
            title="Test News",
            content="This is a test news",
            date=timezone.now(),
        )

    def test_news_str(self):
        self.assertEqual(str(self.news), "Test News")

    def test_news_was_published_recently(self):
        self.assertTrue(self.news.was_published_recently())

    def test_news_was_published_recently_future(self):
        self.news.date = timezone.now() + datetime.timedelta(days=1)
        self.assertFalse(self.news.was_published_recently())

    def test_news_was_published_recently_old(self):
        self.news.date = timezone.now() - datetime.timedelta(days=15)
        self.assertFalse(self.news.was_published_recently())


class ContactMessageModelTestCase(TestCase):
    def setUp(self):
        self.message = ContactMessage.objects.create(
            subject="Test Subject",
            email="from@example.com",
            message="This is a test message",
            date=timezone.now(),
        )

    def test_contact_message_str(self):
        self.assertEqual(str(self.message), "Test Subject")

    def test_contact_message_create_email_message(self):
        email_message = self.message.create_email_message()
        self.assertEqual(email_message.subject, f"Contact message from {self.message.email}")
        self.assertEqual(
            email_message.body,
            f"Subject: {self.message.subject}\n\nFrom: {self.message.email}\n\nMessage: {self.message.message}",
        )
        self.assertEqual(email_message.from_email, "webmaster@localhost")
