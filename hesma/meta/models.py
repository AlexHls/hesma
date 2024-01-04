from django.db import models


class DOI(models.Model):
    doi = models.URLField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.doi}"

    class Meta:
        ordering = ["-created"]
        verbose_name = "DOI"


class Keyword(models.Model):
    keyword = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.keyword}"
