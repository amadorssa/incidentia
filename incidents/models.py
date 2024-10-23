import datetime
from django.db import models
from django.utils import timezone
#from markdownx.models import MarkdownxField

class Incident(models.Model):
    incident_text = models.CharField(max_length=200)
    user_creator = models.CharField(max_length=16) #Cambiar por usuario con sesion iniciada
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    # description = Markdownx(null=True, blank=True)  # Cambiar para cambiar a Markdownx 
    description = models.TextField(null=True, blank=True) 
    
    #Regresar una descripcion del incidente
    def __str__(self):
        return f"{self.incident_text} (by {self.user_creator} on {self.pub_date.strftime('%Y-%m-%d')})"

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
