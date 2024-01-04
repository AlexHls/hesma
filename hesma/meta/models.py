from django.db import models


class DOI(models.Model):
    doi = models.URLField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doi}"

    class Meta:
        ordering = ["-created"]
        verbose_name = "DOI"
