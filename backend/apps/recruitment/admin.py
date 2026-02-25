from django.contrib import admin
from django.utils.html import format_html

from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "location", "job_type", "published_at", "updated_at")
    list_filter = ("status", "job_type", "department")
    search_fields = ("title", "location", "department")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at", "-created_at")

    actions = ["make_published", "make_closed"]

    @admin.action(description="Mark selected jobs as Published")
    def make_published(self, request, queryset):
        queryset.update(status=Job.Status.PUBLISHED)

    @admin.action(description="Mark selected jobs as Closed")
    def make_closed(self, request, queryset):
        queryset.update(status=Job.Status.CLOSED)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "job", "status", "created_at", "cv_link")
    list_filter = ("status", "created_at", "job")
    search_fields = ("full_name", "email", "job__title")
    autocomplete_fields = ("job",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Candidate", {"fields": ("job", "full_name", "email", "phone")}),
        ("Application", {"fields": ("cover_letter", "cv", "created_at")}),
        ("Recruitment workflow", {"fields": ("status", "internal_notes")}),
    )

    actions = ["mark_in_review", "mark_shortlisted", "mark_rejected", "mark_hired"]

    def cv_link(self, obj):
        if not obj.cv:
            return "-"
        return format_html('<a href="{}" target="_blank" rel="noopener">Download</a>', obj.cv.url)

    cv_link.short_description = "CV"

    @admin.action(description="Set status: In review")
    def mark_in_review(self, request, queryset):
        queryset.update(status=JobApplication.Status.IN_REVIEW)

    @admin.action(description="Set status: Shortlisted")
    def mark_shortlisted(self, request, queryset):
        queryset.update(status=JobApplication.Status.SHORTLISTED)

    @admin.action(description="Set status: Rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(status=JobApplication.Status.REJECTED)

    @admin.action(description="Set status: Hired")
    def mark_hired(self, request, queryset):
        queryset.update(status=JobApplication.Status.HIRED)