from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.leads.forms import ContactLeadForm


class HomeView(TemplateView):
    template_name = "core/home.html"


class AboutView(TemplateView):
    template_name = "core/about.html"


class ServicesView(TemplateView):
    template_name = "core/services.html"


class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactLeadForm
    success_url = reverse_lazy("contact_thanks")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ContactThanksView(TemplateView):
    template_name = "core/contact_thanks.html"


class PortalHomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/portal_home.html"
