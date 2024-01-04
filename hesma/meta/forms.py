from bootstrap_modal_forms.forms import BSModalModelForm

from hesma.meta.models import DOI


class DOIForm(BSModalModelForm):
    class Meta:
        model = DOI
        fields = ["doi"]
        labels = {"doi": "DOI"}
        help_texts = {"doi": "Enter a DOI to add to the database."}
        error_messages = {"doi": {"unique": "This DOI is already in the database."}}
