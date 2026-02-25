from django.conf import settings
from django.db import models
from django.utils import timezone


class Lead(models.Model):
    class Type(models.TextChoices):
        CONTACT = "contact", "Contact enquiry"
        NEWSLETTER = "newsletter", "Newsletter subscription"

    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In progress"
        CLOSED = "closed", "Closed"

    lead_type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)

    # Consent / compliance
    marketing_consent = models.BooleanField(default=False)

    # Tracking / audit
    source_path = models.CharField(max_length=255, blank=True)     # e.g. "/contact/"
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    # Internal workflow
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_leads",
    )
    internal_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["lead_type", "status", "created_at"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self) -> str:
        return f"{self.get_lead_type_display()} - {self.email}"

    def close(self):
        self.status = self.Status.CLOSED
        self.closed_at = timezone.now()
        self.save(update_fields=["status", "closed_at", "updated_at"])