from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Student, Teacher, NumGroup

class UserForm(UserCreationForm, forms.ModelForm):
    def __init__(self, *argv, **kwargs):
        super().__init__(*argv, **kwargs)
        self.fields['first_name'].required = True
        self.fields['password1'].help_text = '<ul><li>Пароль не должен быть слишком похож на другую вашу личную информацию.</li><li>Ваш пароль должен содержать как минимум 8 символов.</li><li>Пароль не может состоять только из цифр.</li></ul>'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class StudentForm(forms.ModelForm):
    def __init__(self, *argv, **kwargs):
        super().__init__(*argv, **kwargs)
        self.fields['num_group'].widget.attrs.update({'class': 'test'})
        self.fields['num_group'].empty_label = None
        self.fields['num_group'].initial = 1

    class Meta:
        model = Student
        exclude = ('user',)

    def save(self, user, **kwargs):
        data = super().save(commit=False)
        data.user = user
        data.save()
        return data

class TeacherForm(forms.ModelForm):
    num_groups = forms.ModelMultipleChoiceField(
            label='Номера групп',
            queryset=NumGroup.objects.all(),
            widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Teacher
        exclude = ('user',)

    def save(self, user, **kwargs):
        data = super().save(commit=False)
        data.user = user
        data.save()
        self.save_m2m()
        return data