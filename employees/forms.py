from django import forms
from django.contrib.auth.models import User
from .models import Employee, Department

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'position']  

    department = forms.ModelChoiceField(queryset=Department.objects.all())

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter employee name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter employee email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter employee phone number'}))
    position = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter employee position'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
