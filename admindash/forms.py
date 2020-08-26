from django import forms
from .models import SendEmail

class SendEmailForm(forms.ModelForm):

    class Meta:
        model = SendEmail
        fields = '__all__'