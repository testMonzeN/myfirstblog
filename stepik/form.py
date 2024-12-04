from django import forms
from .models import Taskpy
from .models import Decisionpy
from .models import Taskjs
from .models import Decisionjs


class TaskForm(forms.ModelForm):
    class Meta:
        model = Taskpy
        fields = ('title', 'text')

class DecisionForm(forms.ModelForm):
    class Meta:
        model = Decisionpy
        fields = ('task', 'text')

class TaskFormJs(forms.ModelForm):
    class Meta:
        model = Taskjs
        fields = ('title', 'text')

class DecisionFormJs(forms.ModelForm):
    class Meta:
        model = Decisionjs
        fields = ('task', 'text')