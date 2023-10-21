from django.test import TestCase

from hesma.pages.models import FAQ, FAQTopic


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
