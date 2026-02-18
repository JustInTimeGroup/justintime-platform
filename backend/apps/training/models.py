from django.db import models


class Training(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=255)
    description = models.TextField()

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)

    capacity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.DRAFT)

    # Payment-ready fields (can be unused initially)
    price_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_currency = models.CharField(max_length=10, default="NGN")
    payments_enabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title


class TrainingRegistration(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="registrations")

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)

    # Payment-ready fields
    payment_reference = models.CharField(max_length=255, blank=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_currency = models.CharField(max_length=10, default="NGN")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["training", "created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"{self.full_name} → {self.training.title}"
