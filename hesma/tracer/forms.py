from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm

from hesma.meta.models import DOI, Keyword
from hesma.tracer.models import TracerSimulation


class TracerSimulationForm(ModelForm):
    class Meta:
        model = TracerSimulation
        fields = "__all__"
        exclude = ["user", "date"]

    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = ("admin/jsi18n",)

    DOI = forms.ModelMultipleChoiceField(
        queryset=DOI.objects.all(),
        widget=FilteredSelectMultiple("DOI", is_stacked=False),
        label="DOI",
        required=False,
    )

    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        widget=FilteredSelectMultiple("Keywords", is_stacked=False),
        label="Keywords",
        required=False,
    )
