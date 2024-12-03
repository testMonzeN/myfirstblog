from django import forms
from .models import Task
from .models import Decision

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'text')
class DecisionForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = ('task', 'text')