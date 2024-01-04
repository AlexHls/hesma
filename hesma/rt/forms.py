from django.forms import ModelForm

from hesma.rt.models import RTSimulation


class RTSimulationForm(ModelForm):
    class Meta:
        model = RTSimulation
        fields = "__all__"
        exclude = ["user", "date"]
