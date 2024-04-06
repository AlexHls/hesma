from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm

from hesma.meta.models import DOI, Keyword
from hesma.rt.models import RTSimulation, RTSimulationLightcurveFile, RTSimulationSpectrumFile


class RTSimulationForm(ModelForm):
    class Meta:
        model = RTSimulation
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


class RTSimulationLightcurveFileForm(ModelForm):
    generate_interactive_plot = forms.BooleanField(
        required=False, label="Generate interactive plot (may take a while)"
    )

    class Meta:
        model = RTSimulationLightcurveFile
        fields = "__all__"
        exclude = [
            "date",
            "is_valid_hesma_file",
            "interactive_plot",
            "rt_simulation",
        ]


class RTSimulationSpectrumFileForm(ModelForm):
    generate_interactive_plot = forms.BooleanField(
        required=False, label="Generate interactive plot (may take a while)"
    )

    class Meta:
        model = RTSimulationSpectrumFile
        fields = "__all__"
        exclude = [
            "date",
            "is_valid_hesma_file",
            "interactive_plot",
            "rt_simulation",
        ]
