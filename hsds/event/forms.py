from django import forms
from admission.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'date', 'time', 'cash')


class CashForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'cash')
