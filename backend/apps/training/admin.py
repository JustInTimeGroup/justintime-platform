from django.contrib import admin

from .models import Training, TrainingRegistration


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "start_date", "location", "capacity", "payments_enabled", "created_at")
    list_filter = ("status", "payments_enabled", "created_at")
    search_fields = ("title", "location")
    readonly_fields = ("created_at",)


@admin.register(TrainingRegistration)
class TrainingRegistrationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "training", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "training__title")
    readonly_fields = ("created_at",)
