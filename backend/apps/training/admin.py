from django.contrib import admin
from .models import Training, TrainingRegistration


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "start_date", "end_date", "location", "capacity", "payments_enabled")
    list_filter = ("status", "payments_enabled", "location")
    search_fields = ("title", "location")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-start_date", "-published_at", "-created_at")


@admin.register(TrainingRegistration)
class TrainingRegistrationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "training", "status", "created_at")
    list_filter = ("status", "created_at", "training")
    search_fields = ("full_name", "email", "training__title")
    autocomplete_fields = ("training",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Registrant", {"fields": ("training", "full_name", "email", "phone", "organisation")}),
        ("Workflow", {"fields": ("status",)}),
        ("Payment-ready", {"fields": ("payment_reference", "payment_status")}),
        ("Meta", {"fields": ("created_at",)}),
    )