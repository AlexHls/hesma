from bootstrap_modal_forms.forms import BSModalModelForm

from hesma.meta.models import DOI, Keyword


class DOIForm(BSModalModelForm):
    class Meta:
        model = DOI
        fields = ["doi", "author", "title", "date"]
        labels = {"doi": "DOI"}
        help_texts = {"doi": "Enter a DOI to add to the database."}
        error_messages = {"doi": {"unique": "This DOI is already in the database."}}


class KeywordForm(BSModalModelForm):
    class Meta:
        model = Keyword
        fields = ["keyword"]
        labels = {"keyword": "Keyword"}
        help_texts = {"keyword": "Enter a keyword to add to the database."}
        error_messages = {"keyword": {"unique": "This keyword is already in the database."}}
