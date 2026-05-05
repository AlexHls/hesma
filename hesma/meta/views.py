from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy

from hesma.meta.forms import DOIForm, KeywordForm
from hesma.utils.permissions import GroupRequiredMixin


class DOICreateViewHydro(GroupRequiredMixin, BSModalCreateView):
    group_name = "hydro_user"
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("hydro:hydro_upload")


class DOICreateViewHydroEdit(GroupRequiredMixin, BSModalCreateView):
    group_name = "hydro_user"
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("hydro:hydro_edit")


class DOICreateViewRT(GroupRequiredMixin, BSModalCreateView):
    group_name = "rt_user"
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("rt:rt_upload")


class DOICreateViewRTEdit(GroupRequiredMixin, BSModalCreateView):
    group_name = "rt_user"
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("rt:rt_edit")


class DOICreateViewTracer(GroupRequiredMixin, BSModalCreateView):
    group_name = "tracer_user"
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("tracer:tracer_upload")


class DOICreateViewTracerEdit(GroupRequiredMixin, BSModalCreateView):
    group_name = "tracer_user"
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("tracer:tracer_edit")


class KeywordCreateViewHydro(GroupRequiredMixin, BSModalCreateView):
    group_name = "hydro_user"
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
    success_url = reverse_lazy("hydro:hydro_upload")


class KeywordCreateViewHydroEdit(GroupRequiredMixin, BSModalCreateView):
    group_name = "hydro_user"
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
    success_url = reverse_lazy("hydro:hydro_edit")


class KeywordCreateViewRT(GroupRequiredMixin, BSModalCreateView):
    group_name = "rt_user"
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
    success_url = reverse_lazy("rt:rt_upload")


class KeywordCreateViewRTEdit(GroupRequiredMixin, BSModalCreateView):
    group_name = "rt_user"
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
    success_url = reverse_lazy("rt:rt_edit")


class KeywordCreateViewTracer(GroupRequiredMixin, BSModalCreateView):
    group_name = "tracer_user"
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
    success_url = reverse_lazy("tracer:tracer_upload")


class KeywordCreateViewTracerEdit(GroupRequiredMixin, BSModalCreateView):
    group_name = "tracer_user"
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
    success_url = reverse_lazy("tracer:tracer_edit")
