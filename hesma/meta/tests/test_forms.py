import datetime

from django.test import TestCase

from hesma.meta.forms import DOIForm, KeywordForm
from hesma.meta.models import DOI, Keyword


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


class KeywordFormTestCase(TestCase):
    def setUp(self):
        self.keyword = Keyword.objects.create(keyword="Test Keyword")

    def test_keyword_form_valid(self):
        form = KeywordForm({"keyword": "Test Keyword 2"})
        self.assertTrue(form.is_valid())

    def test_keyword_form_invalid(self):
        form = KeywordForm({"keyword": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["keyword"], ["This field is required."])

    def test_keyword_form_unique(self):
        form = KeywordForm({"keyword": "Test Keyword"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["keyword"], ["This keyword is already in the database."])
