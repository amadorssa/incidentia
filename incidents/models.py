import datetime
from django.db import models
from django.utils import timezone

class Incident(models.Model):
    incident_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    description = models.TextField(null=True, blank=True) 
    
    def __str__(self):
        return self.incident_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
