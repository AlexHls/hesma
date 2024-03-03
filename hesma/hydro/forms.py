from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm

from hesma.hydro.models import HydroSimulation, HydroSimulation1DModelFile
from hesma.meta.models import DOI, Keyword


class HydroSimulationForm(ModelForm):
    class Meta:
        model = HydroSimulation
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


class HydroSimulation1DModelFileForm(ModelForm):
    class Meta:
        model = HydroSimulation1DModelFile
        fields = "__all__"
        exclude = ["date", "is_valid_hesma_file"]
