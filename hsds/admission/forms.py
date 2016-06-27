from django import forms
from models import AdmissionType, Expenses


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionType
        fields = ('type', 'price')


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ('name', 'type', 'notes', 'percent', 'cost')