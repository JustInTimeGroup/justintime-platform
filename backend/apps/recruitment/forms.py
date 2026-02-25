from django import forms
from django.core.exceptions import ValidationError

from .models import JobApplication


MAX_CV_SIZE_MB = 5
ALLOWED_MIME = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["full_name", "email", "phone", "cover_letter", "cv"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "input", "placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "Email address"}),
            "phone": forms.TextInput(attrs={"class": "input", "placeholder": "Phone (optional)"}),
            "cover_letter": forms.Textarea(attrs={"class": "textarea", "placeholder": "Optional cover letter"}),
        }

    def clean_cv(self):
        f = self.cleaned_data.get("cv")
        if not f:
            return f

        # Size validation
        max_bytes = MAX_CV_SIZE_MB * 1024 * 1024
        if f.size > max_bytes:
            raise ValidationError(f"CV file must be {MAX_CV_SIZE_MB}MB or smaller.")

        # Content-type validation (best-effort; browsers can lie, but still useful)
        ctype = getattr(f, "content_type", "") or ""
        if ctype and ctype not in ALLOWED_MIME:
            raise ValidationError("Unsupported file type. Upload PDF, DOC, or DOCX.")

        return f