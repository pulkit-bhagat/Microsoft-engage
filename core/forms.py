from django import forms
from django.forms import fields
from .models import AssignmentSolution

class SolutionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSolution
        fields = ('file', )