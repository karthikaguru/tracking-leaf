from django import forms
from .models import  Project, Stage, Expense
from frontsite.models import CustomUser
from decimal import Decimal
from datetime import date



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client', 'name', 'budget', 'length', 'breadth', 'status']  
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter budget'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter length in feet'}),  
            'breadth': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter breadth in feet'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
 


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['project', 'name', 'due_date', 'progress', 'status', 'start_date', 'end_date', 'stage_type']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter stage name'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter progress percentage'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'stage_type': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < date.today():
            raise forms.ValidationError("Start date cannot be earlier than today's date.")
        return start_date



class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['project', 'stage',  'amount_spent', 'date']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'stage': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'amount_spent': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'autocomplete': 'off'}),
        }
