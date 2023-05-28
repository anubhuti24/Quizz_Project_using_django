from django.utils import timezone
from datetime import datetime
from django.db import models


class Quiz(models.Model):
    question = models.CharField(max_length=255, null=False)
    options = models.JSONField()
    right_answer = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    STATUS_CHOICES = [
        ('inactive', 'Inactive'),
        ('active', 'Active'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def save(self, *args, **kwargs):
        current_time_str = timezone.localtime(timezone.now())
        current_time = current_time_str.strftime("%Y-%m-%d %H:%M:%S")
        if self.start_date > current_time:
            self.status = 'inactive'
        elif self.start_date <= current_time <= self.end_date:
            self.status = 'active'
        else:
            self.status = 'finished'
        super().save(*args, **kwargs)