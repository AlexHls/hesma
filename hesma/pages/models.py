import datetime

from django.conf import settings
from django.core.mail import EmailMessage
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
    sticky = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        # Return False if the date is in the future
        if self.date > timezone.now():
            return False
        return self.date >= timezone.now() - datetime.timedelta(days=14)


class ContactMessage(models.Model):
    subject = models.CharField(max_length=300)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.subject

    def create_email_message(self):
        return EmailMessage(
            subject=f"Contact message from {self.email}",
            body=f"Subject: {self.subject}\n\nFrom: {self.email}\n\nMessage: {self.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.CONTACT_EMAILS,
        )
