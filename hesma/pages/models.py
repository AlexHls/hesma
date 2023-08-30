from django.db import models


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
