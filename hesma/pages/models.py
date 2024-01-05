import datetime

from django.db import models
from django.utils import timezone


class FAQTopic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    topic = models.ForeignKey(FAQTopic, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.question


class News(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title

    def was_published_recently(self):
        # Return False if the date is in the future
        if self.date > timezone.now():
            return False
        return self.date >= timezone.now() - datetime.timedelta(days=14)
