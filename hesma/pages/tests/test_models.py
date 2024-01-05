import datetime

from django.test import TestCase
from django.utils import timezone

from hesma.pages.models import FAQ, FAQTopic, News


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
