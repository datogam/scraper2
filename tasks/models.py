from django.db import models
from django.utils import timezone


class CeleryTask(models.Model):
    task_id = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)