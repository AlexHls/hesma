import datetime

import hesmapy.base as hp
from django.conf import settings
from django.db import models
from django.utils import timezone

from config.settings.base import hydro_fs, meta_fs
from hesma.meta.models import DOI, Keyword


class HydroSimulation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    reference = models.URLField(max_length=200, blank=True)
    date = models.DateTimeField("date uploaded")
    author = models.CharField(max_length=300, blank=True)

    readme = models.FileField(storage=meta_fs, blank=True)
    doi = models.ManyToManyField(DOI, blank=True, name="DOI")
    keywords = models.ManyToManyField(Keyword, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        # Return False if the date is in the future
        if self.date > timezone.now():
            return False
        return self.date >= timezone.now() - datetime.timedelta(days=14)


class HydroSimulation1DModelFile(models.Model):
    hydro_simulation = models.ForeignKey(HydroSimulation, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(storage=hydro_fs)
    date = models.DateTimeField("date uploaded")
    description = models.TextField(blank=True)
    is_valid_hesma_file = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        # Return False if the date is in the future
        if self.date > timezone.now():
            return False
        return self.date >= timezone.now() - datetime.timedelta(days=14)

    def get_plot_html(self):
        model = hp.load_hydro_1d(self.file.path)
        fig = model.plot()
        return fig.to_html(
            include_plotlyjs="cdn",
            full_html=False,
            default_height=720,
            default_width=1080,
        )
