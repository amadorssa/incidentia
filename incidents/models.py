import datetime
from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField

class Incident(models.Model):
    incident_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    description = MarkdownxField(null=True, blank=True)  # Campo de descripción con soporte Markdown
    
    def __str__(self):
        return self.incident_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
