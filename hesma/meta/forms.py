from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from hesma.meta.models import DOI, Keyword


class DOIForm(BSModalModelForm):
    doi = forms.URLField(
        assume_scheme="https",
        label="DOI",
        help_text="Enter a DOI to add to the database.",
        error_messages={"unique": "This DOI is already in the database."},
    )

    class Meta:
        model = DOI
        fields = ["doi", "author", "title", "date"]


class KeywordForm(BSModalModelForm):
    class Meta:
        model = Keyword
        fields = ["keyword"]
        labels = {"keyword": "Keyword"}
        help_texts = {"keyword": "Enter a keyword to add to the database."}
        error_messages = {"keyword": {"unique": "This keyword is already in the database."}}
