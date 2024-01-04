import datetime

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

from config.settings.base import meta_fs
from hesma.meta.models import DOI


class HydroSimulation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    reference = models.URLField(max_length=200, blank=True)
    date = models.DateTimeField("date uploaded")
    author = models.CharField(max_length=300, blank=True)

    readme = models.FileField(storage=meta_fs, blank=True)
    doi = models.ManyToManyField(DOI, blank=True, name="DOI")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        # Return False if the date is in the future
        if self.date > timezone.now():
            return False
        return self.date >= timezone.now() - datetime.timedelta(days=14)


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
    )
