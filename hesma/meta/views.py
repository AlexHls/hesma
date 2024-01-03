from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy

from hesma.meta.models import DOIForm


class DOICreateViewHydro(BSModalCreateView):
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("hydro:hydro_upload")
