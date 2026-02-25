from django import forms

from .models import TrainingRegistration


class TrainingRegistrationForm(forms.ModelForm):
    class Meta:
        model = TrainingRegistration
        fields = ["full_name", "email", "phone", "organisation"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "input", "placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "Email address"}),
            "phone": forms.TextInput(attrs={"class": "input", "placeholder": "Phone (optional)"}),
            "organisation": forms.TextInput(attrs={"class": "input", "placeholder": "Organisation (optional)"}),
        }