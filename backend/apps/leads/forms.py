from django import forms

from .models import Lead


class ContactLeadForm(forms.ModelForm):
    """
    Main contact form used across the site.
    Includes hidden honeypot for spam protection.
    """

    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Lead
        fields = ["full_name", "email", "phone", "subject", "message", "marketing_consent"]

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "input", "placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "Email address"}),
            "phone": forms.TextInput(attrs={"class": "input", "placeholder": "Phone (optional)"}),
            "subject": forms.TextInput(attrs={"class": "input", "placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"class": "textarea", "placeholder": "How can we help?"}),
        }

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value


class NewsletterForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Lead
        fields = ["email", "marketing_consent"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "Your email"}),
        }

    def clean_honeypot(self):
        if self.cleaned_data.get("honeypot"):
            raise forms.ValidationError("Spam detected.")
        return ""