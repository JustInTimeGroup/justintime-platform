from django.contrib import admin

from .models import ContactLead, NewsletterSubscriber


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "status", "created_at", "handled_by")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "phone", "subject")
    readonly_fields = ("created_at",)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "subscribed_at")
    list_filter = ("is_active", "subscribed_at")
    search_fields = ("email",)
    readonly_fields = ("subscribed_at",)
