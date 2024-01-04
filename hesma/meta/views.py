from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy

from hesma.meta.forms import DOIForm


class DOICreateViewHydro(BSModalCreateView):
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("hydro:hydro_upload")


class DOICreateViewHydroEdit(BSModalCreateView):
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("hydro:hydro_edit")


class DOICreateViewRT(BSModalCreateView):
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("rt:rt_upload")


class DOICreateViewRTEdit(BSModalCreateView):
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("rt:rt_edit")


class DOICreateViewTracer(BSModalCreateView):
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("tracer:tracer_upload")


class DOICreateViewTracerEdit(BSModalCreateView):
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("tracer:tracer_edit")
