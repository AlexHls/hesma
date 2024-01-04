from django.forms import ModelForm

from hesma.tracer.models import TracerSimulation


class TracerSimulationForm(ModelForm):
    class Meta:
        model = TracerSimulation
        fields = "__all__"
        exclude = ["user", "date"]
