import uuid
from pathlib import Path

from django.conf import settings
from django.db import models


def cv_upload_path(instance: "JobApplication", filename: str) -> str:
    # Do not trust filename; keep extension only
    ext = Path(filename).suffix.lower()[:10]
    return f"recruitment/cv/{instance.job_id}/{instance.id}{ext}"


class Job(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    employment_type = models.CharField(max_length=100, blank=True)  # e.g. Full-time, Contract
    description = models.TextField()

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.DRAFT)

    published_at = models.DateTimeField(null=True, blank=True)
    closes_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title


class JobApplication(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_REVIEW = "in_review", "In review"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"
        HIRED = "hired", "Hired"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)

    cover_letter = models.TextField(blank=True)

    cv_file = models.FileField(upload_to=cv_upload_path)

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.NEW)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_applications",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["job", "created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"{self.full_name} → {self.job.title}"
