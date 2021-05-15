import datetime
from django import forms
from .models import Task, Answer

class EditTaskForm(forms.ModelForm):
    date_opening = forms.DateTimeField(
        label='Дата открытия',
        input_formats=['%m/%d/%Y'],
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        required=False
    )
    date_end = forms.DateTimeField(
        initial=format(datetime.date.today(),'%m/%d/%Y'),
        label='Дата закрытия',
        input_formats=['%m/%d/%Y'], 
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )

    class Meta:
        model = Task
        fields = ('name', 'task', 'date_end', 'active', 'date_opening')

    def clean_date_opening(self):
        active = self.cleaned_data['active']
        date_open = self.cleaned_data['date_opening']
        date_end = self.cleaned_data['date_end']

        if (not active and date_open and date_open >= date_end):
            raise forms.ValidationError('Дата открытия не может быть меньше или равна даты закрытия')

        return date_open

class TaskForm(forms.ModelForm):
    date_opening = forms.DateTimeField(
        label='Дата открытия',
        input_formats=['%m/%d/%Y'],
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        required=False
    )
    date_end = forms.DateTimeField(
        initial=format(datetime.date.today(),'%m/%d/%Y'),
        label='Дата закрытия',
        input_formats=['%m/%d/%Y'], 
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )

    def __init__(self, *argv, **kwargs):
        super().__init__(*argv, **kwargs)
        self.fields['subject'].widget.attrs['disabled'] = 'disabled'

    def clean_date_opening(self):
        active = self.cleaned_data['active']
        date_open = self.cleaned_data['date_opening']
        date_end = self.cleaned_data['date_end']

        if (not active and date_open and date_open >= date_end):
            raise forms.ValidationError('Дата открытия не может быть меньше или равна даты закрытия')

        return date_open

    class Meta:
        model = Task
        exclude = ('date_start',)
        widgets = {'teacher': forms.HiddenInput()}


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('name', 'answer')
