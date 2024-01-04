import datetime

from django.test import TestCase

from hesma.meta.models import DOI


class DOITestCase(TestCase):
    def setUp(self):
        self.doi = DOI.objects.create(
            doi="https://doi.org/10.48550/arXiv.2310.19669",
            author="Test Author",
            title="Test Title",
            date=datetime.date.today(),
        )

    def test_doi_str(self):
        self.assertEqual(str(self.doi), "https://doi.org/10.48550/arXiv.2310.19669")

    def test_doi_creation(self):
        self.assertIsInstance(self.doi, DOI)
        self.assertEqual(self.doi.author, "Test Author")
        self.assertEqual(self.doi.title, "Test Title")
        self.assertEqual(self.doi.date, datetime.date.today())

    def test_doi_unique(self):
        with self.assertRaises(Exception):
            DOI.objects.create(
                doi="https://doi.org/10.48550/arXiv.2310.19669",
                author="Test Author 2",
                title="Test Title 2",
                date=datetime.date.today(),
            )
