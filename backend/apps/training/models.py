from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Training(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)

    summary = models.TextField(blank=True)
    description = models.TextField()

    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    duration_label = models.CharField(max_length=120, blank=True)  # e.g. "2 days", "6 weeks"

    capacity = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)

    # Payment-ready (not enabled yet)
    price_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="GBP")
    payments_enabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date", "-published_at", "-created_at", "-id"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:220] or "training"
            slug = base
            i = 2
            while Training.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug

        if self.status == Training.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    @property
    def is_open(self) -> bool:
        return self.status == Training.Status.PUBLISHED


class TrainingRegistration(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="registrations")

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    organisation = models.CharField(max_length=200, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    # Payment-ready placeholders (we’ll wire later)
    payment_reference = models.CharField(max_length=120, blank=True)
    payment_status = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        unique_together = [("training", "email")]  # avoid duplicate signups per training/email

    def __str__(self) -> str:
        return f"{self.full_name} → {self.training.title}"