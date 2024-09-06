from django import forms
from .models import Certification


class RevokeCertificationForm(forms.ModelForm):
    model = Certification
    reason = forms.CharField(widget=forms.Textarea, required=True)

class EmailCertificationForm(forms.Form):
    recipient_email = forms.EmailField()
    