from django.contrib import admin
from django.utils.html import format_html

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "lead_type",
        "status",
        "email",
        "full_name",
        "phone",
        "source_path",
        "assigned_to",
        "created_at",
    )
    list_filter = ("lead_type", "status", "created_at")
    search_fields = ("email", "full_name", "phone", "subject", "message", "source_path")
    autocomplete_fields = ("assigned_to",)
    readonly_fields = ("created_at", "updated_at", "closed_at", "ip_address", "user_agent")

    fieldsets = (
        ("Lead", {"fields": ("lead_type", "status", "assigned_to")}),
        ("Contact details", {"fields": ("full_name", "email", "phone")}),
        ("Enquiry", {"fields": ("subject", "message")}),
        ("Consent", {"fields": ("marketing_consent",)}),
        ("Tracking", {"fields": ("source_path", "ip_address", "user_agent")}),
        ("Internal", {"fields": ("internal_notes",)}),
        ("Meta", {"fields": ("created_at", "updated_at", "closed_at")}),
    )

    actions = ["mark_in_progress", "mark_closed"]

    @admin.action(description="Mark selected as In progress")
    def mark_in_progress(self, request, queryset):
        queryset.update(status=Lead.Status.IN_PROGRESS)

    @admin.action(description="Mark selected as Closed")
    def mark_closed(self, request, queryset):
        queryset.update(status=Lead.Status.CLOSED)