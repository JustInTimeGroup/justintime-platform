from django import forms
from .models import ContactLead


class ContactLeadForm(forms.ModelForm):
    class Meta:
        model = ContactLead
        fields = ["full_name", "email", "phone", "subject", "message"]

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "input", "placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "Email address"}),
            "phone": forms.TextInput(attrs={"class": "input", "placeholder": "Phone (optional)"}),
            "subject": forms.TextInput(attrs={"class": "input", "placeholder": "Subject (optional)"}),
            "message": forms.Textarea(attrs={"class": "textarea", "placeholder": "How can we help?"}),
        }