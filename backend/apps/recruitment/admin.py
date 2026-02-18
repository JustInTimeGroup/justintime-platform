from django.contrib import admin

from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "status", "published_at", "closes_at", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "location")
    readonly_fields = ("created_at",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "job", "status", "created_at", "reviewed_by")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "phone", "job__title")
    readonly_fields = ("created_at",)
