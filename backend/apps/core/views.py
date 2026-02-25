from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

from apps.leads.forms import ContactLeadForm
from apps.leads.models import Lead
from apps.leads.forms import NewsletterForm
from apps.leads.utils import extract_request_meta

from django.http import HttpResponse
from apps.leads.rate_limit import hit
from django.utils import timezone

class HomeView(TemplateView):
    template_name = "core/home.html"


class AboutView(TemplateView):
    template_name = "core/about.html"


class ServicesView(TemplateView):
    template_name = "core/services.html"


class PortalHomeView(TemplateView):
    template_name = "core/portal_home.html"


class ContactThanksView(TemplateView):
    template_name = "core/contact_thanks.html"


class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactLeadForm

    def form_valid(self, form):
        lead: Lead = form.save(commit=False)
        lead.lead_type = Lead.Type.CONTACT

        # attach metadata
        meta = extract_request_meta(self.request)
        # Rate limit: 5 submissions per 10 minutes per IP
        if not hit(key=f"contact:{meta['ip_address']}", limit=5, window_seconds=600):
            return HttpResponse("Too many requests. Please try again later.", status=429)
        lead.ip_address = meta["ip_address"]
        lead.user_agent = meta["user_agent"]
        lead.source_path = meta["source_path"]

        recent = Lead.objects.filter(
            lead_type=Lead.Type.CONTACT,
            email__iexact=lead.email,
            subject=lead.subject,
            message=lead.message,
        ).order_by("-created_at").first()

        if recent and (timezone.now() - recent.created_at).total_seconds() < 600:
            return redirect("contact_thanks")

        lead.save()

        # email notification
        send_mail(
            subject=f"New contact enquiry: {lead.subject or 'Website enquiry'}",
            message=(
                f"Name: {lead.full_name}\n"
                f"Email: {lead.email}\n"
                f"Phone: {lead.phone}\n\n"
                f"{lead.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
            fail_silently=True,
        )

        return redirect("contact_thanks")
    
class NewsletterSignupView(FormView):
    form_class = NewsletterForm
    http_method_names = ["post"]

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.lead_type = Lead.Type.NEWSLETTER

        meta = extract_request_meta(self.request)

        # Rate limit: 10 signups per 10 minutes per IP
        if not hit(key=f"newsletter:{meta['ip_address']}", limit=10, window_seconds=600):
            return HttpResponse("Too many requests. Please try again later.", status=429)
        
        lead.ip_address = meta["ip_address"]
        lead.user_agent = meta["user_agent"]
        lead.source_path = meta["source_path"]

        # Duplicate suppression: if already subscribed, don’t create another row
        existing = Lead.objects.filter(lead_type=Lead.Type.NEWSLETTER, email__iexact=lead.email).first()
        if existing:
            return redirect("/")

        lead.save()
        return redirect("newsletter_thanks")
    
class NewsletterThanksView(TemplateView):
    template_name = "core/newsletter_thanks.html"