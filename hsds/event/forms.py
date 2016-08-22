from django import forms
from admission.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'time': forms.TimeInput(attrs={'class': 'timepicker'}),
        }
        fields = ('organization', 'name', 'type', 'date', 'time', 'cash', 'admin_fee')


class CashForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'cash')
