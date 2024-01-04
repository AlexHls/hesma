from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm

from hesma.hydro.models import HydroSimulation
from hesma.meta.models import DOI


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
