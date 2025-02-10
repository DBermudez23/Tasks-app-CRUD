from django import forms
from .models import Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = { #Styles (Bootstrap classes)
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Write the task title:'}),
            'description' : forms.TextInput(attrs={'class' : 'form-control py-5', 'placeholder' : 'Wirte the description of the task...'}),
            'important' : forms.CheckboxInput(attrs={'class' : 'form-check-input m-auto'})
        }