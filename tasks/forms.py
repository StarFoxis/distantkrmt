from django import forms

from .models import Task, Answer

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'task', 'active', 'date_opening')

class TaskForm(forms.ModelForm):
    def __init__(self, *argv, **kwargs):
        super().__init__(*argv, **kwargs)
        self.fields['subject'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Task
        exclude = ('date_start',)
        widgets = {'teacher': forms.HiddenInput()}


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('name', 'answer')