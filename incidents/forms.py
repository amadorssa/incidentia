from django import forms
from .models import Incident, Attachment
from django.core.exceptions import ValidationError 
from django.utils import timezone 
from django.forms.models import inlineformset_factory


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['incident_text', 'description', 'prioridad', 'category', 'start_date', 'due_date']  
        labels = {
            'incident_text': 'Nombre',
            'user_creator': 'Agregado por',
            'description': 'Descripción',
            'start_date': 'Fecha de inicio',
            'due_date': 'Fecha de vencimiento',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        due_date = cleaned_data.get("due_date")
        pub_date = self.instance.pub_date if self.instance.pk else timezone.now()

        if start_date and due_date and start_date > due_date:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de vencimiento.")

        if due_date and start_date and due_date < start_date:
            raise ValidationError("La fecha de vencimiento no puede ser anterior a la fecha de inicio.")

        if start_date and start_date < pub_date:
            raise ValidationError("La fecha de inicio no puede ser anterior a la fecha de publicación.")

        return cleaned_data

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(),
        }


AttachmentFormSet = inlineformset_factory(
    Incident,
    Attachment,
    form=AttachmentForm,
    extra=3,
    can_delete=True
)
