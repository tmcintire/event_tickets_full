from django import forms
from models import AdmissionType, Expenses, EventType, ExpenseType


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionType
        fields = ('event', 'type', 'price')


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ('name', 'type', 'notes', 'percent', 'cost')


class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ('event_type',)


class ExpenseTypeForm(forms.ModelForm):
    class Meta:
        model = ExpenseType
        fields = ('expense_type',)