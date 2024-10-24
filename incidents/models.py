import datetime
from django.db import models
from django.utils import timezone
#from markdownx.models import MarkdownxField

class Incident(models.Model):
    incident_text = models.CharField(max_length=200)
    user_creator = models.CharField(max_length=16)  # Cambiar por usuario con sesión iniciada
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    description = models.TextField(null=True, blank=True)  # Campo de descripción con soporte Markdown
    
    # Nuevos campos
    start_date = models.DateTimeField('Fecha de inicio', null=True, blank=True)
    due_date = models.DateTimeField('Fecha de vencimiento', null=True, blank=True)

    def __str__(self):
        return f"{self.incident_text} (by {self.user_creator} on {self.pub_date.strftime('%Y-%m-%d')})"