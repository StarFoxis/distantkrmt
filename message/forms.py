from django import forms
from django.contrib.auth.models import User

from .models import Message

class CreateMessageForm(forms.ModelForm):
    def __init__(self, *argv, **kwargs):
        super().__init__(*argv, **kwargs)

        self.fields['sender'].widget = forms.HiddenInput()
        self.fields['resipient'].widget = forms.HiddenInput()

    class Meta:
        model = Message
        fields = ('sender', 'resipient', 'message')