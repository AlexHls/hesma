import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from config.settings.base import meta_fs
from hesma.meta.models import DOI, Keyword


class RTSimulation(models.Model):
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
