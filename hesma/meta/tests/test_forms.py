import datetime

from django.test import TestCase

from hesma.meta.forms import DOIForm
from hesma.meta.models import DOI


class DOIFormTestCase(TestCase):
    def setUp(self):
        self.doi = DOI.objects.create(
            doi="https://doi.org/10.48550/arXiv.2310.19669",
            author="Test Author",
            title="Test Title",
            date=datetime.date.today(),
        )

    def test_doi_form_valid(self):
        form = DOIForm(
            {
                "doi": "https://doi.org/10.48550/arXiv.2310.19670",
                "author": "Test Author",
                "title": "Test Title",
                "date": datetime.date.today(),
            }
        )
        self.assertTrue(form.is_valid())

    def test_doi_form_invalid(self):
        form = DOIForm(
            {
                "doi": "Test DOI",
                "author": "Test Author",
                "title": "Test Title",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["doi"], ["Enter a valid URL."])

    def test_doi_form_unique(self):
        form = DOIForm(
            {
                "doi": "https://doi.org/10.48550/arXiv.2310.19669",
                "author": "Test Author 2",
                "title": "Test Title 2",
                "date": datetime.date.today(),
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["doi"], ["This DOI is already in the database."])
