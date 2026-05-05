from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy

from hesma.meta.forms import DOIForm, KeywordForm
from hesma.utils.permissions import GroupRequiredMixin


class RefererSuccessUrlMixin:
    fallback_success_url = "/"

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER", self.fallback_success_url)


class DOICreateViewHydro(GroupRequiredMixin, BSModalCreateView):
    group_name = "hydro_user"
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("hydro:hydro_upload")


class DOICreateViewHydroEdit(RefererSuccessUrlMixin, GroupRequiredMixin, BSModalCreateView):
    group_name = "hydro_user"
    fallback_success_url = reverse_lazy("hydro:hydro_upload")
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."


class DOICreateViewRT(GroupRequiredMixin, BSModalCreateView):
    group_name = "rt_user"
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("rt:rt_upload")


class DOICreateViewRTEdit(RefererSuccessUrlMixin, GroupRequiredMixin, BSModalCreateView):
    group_name = "rt_user"
    fallback_success_url = reverse_lazy("rt:rt_upload")
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."


class DOICreateViewTracer(GroupRequiredMixin, BSModalCreateView):
    group_name = "tracer_user"
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."
    success_url = reverse_lazy("tracer:tracer_upload")


class DOICreateViewTracerEdit(RefererSuccessUrlMixin, GroupRequiredMixin, BSModalCreateView):
    group_name = "tracer_user"
    fallback_success_url = reverse_lazy("tracer:tracer_upload")
    template_name = "meta/create_doi.html"
    form_class = DOIForm
    success_message = "Success: DOI was created."


class KeywordCreateViewHydro(GroupRequiredMixin, BSModalCreateView):
    group_name = "hydro_user"
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
    success_url = reverse_lazy("hydro:hydro_upload")


class KeywordCreateViewHydroEdit(RefererSuccessUrlMixin, GroupRequiredMixin, BSModalCreateView):
    group_name = "hydro_user"
    fallback_success_url = reverse_lazy("hydro:hydro_upload")
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."


class KeywordCreateViewRT(GroupRequiredMixin, BSModalCreateView):
    group_name = "rt_user"
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
    success_url = reverse_lazy("rt:rt_upload")


class KeywordCreateViewRTEdit(RefererSuccessUrlMixin, GroupRequiredMixin, BSModalCreateView):
    group_name = "rt_user"
    fallback_success_url = reverse_lazy("rt:rt_upload")
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."


class KeywordCreateViewTracer(GroupRequiredMixin, BSModalCreateView):
    group_name = "tracer_user"
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
    success_url = reverse_lazy("tracer:tracer_upload")


class KeywordCreateViewTracerEdit(RefererSuccessUrlMixin, GroupRequiredMixin, BSModalCreateView):
    group_name = "tracer_user"
    fallback_success_url = reverse_lazy("tracer:tracer_upload")
    template_name = "meta/create_keyword.html"
    form_class = KeywordForm
    success_message = "Success: Keyword was created."
