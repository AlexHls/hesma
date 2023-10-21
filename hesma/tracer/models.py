import datetime

from django.conf import settings
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

from config.settings.base import meta_fs


class TracerSimulation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    reference = models.URLField(max_length=200, blank=True)
    date = models.DateTimeField("date uploaded")
    author = models.CharField(max_length=300, blank=True)

    readme = models.FileField(storage=meta_fs, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        # Return False if the date is in the future
        if self.date > timezone.now():
            return False
        return self.date >= timezone.now() - datetime.timedelta(days=14)


class TracerSimulationForm(ModelForm):
    class Meta:
        model = TracerSimulation
        fields = "__all__"
        exclude = ["user", "date"]
