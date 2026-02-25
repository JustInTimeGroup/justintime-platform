from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView, FormView

from .forms import JobApplicationForm
from .models import Job, JobApplication

from django.conf import settings
from django.core.mail import send_mail


class PublishedJobsMixin:
    def get_queryset(self):
        qs = Job.objects.all()
        qs = qs.filter(status=Job.Status.PUBLISHED)
        # If published_at is set, do not show future-dated jobs
        qs = qs.filter(published_at__isnull=True) | qs.filter(published_at__lte=timezone.now())
        return qs.order_by("-published_at", "-created_at", "-id")


class JobListView(PublishedJobsMixin, ListView):
    template_name = "recruitment/list.html"
    context_object_name = "jobs"
    paginate_by = 10


class JobDetailView(PublishedJobsMixin, DetailView):
    template_name = "recruitment/detail.html"
    context_object_name = "job"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class JobApplyView(FormView):
    template_name = "recruitment/apply.html"
    form_class = JobApplicationForm

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(
            Job,
            slug=kwargs["slug"],
            status=Job.Status.PUBLISHED,
        )
        # optional future gate
        if self.job.published_at and self.job.published_at > timezone.now():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["job"] = self.job
        return ctx

    def form_valid(self, form):
        application: JobApplication = form.save(commit=False)
        application.job = self.job
        application.save()

        subject = f"New job application: {self.job.title}"
        message = (
            f"New application received.\n\n"
            f"Job: {self.job.title}\n"
            f"Name: {application.full_name}\n"
            f"Email: {application.email}\n"
            f"Phone: {application.phone or '-'}\n\n"
            f"View in admin: /admin/recruitment/jobapplication/\n"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.RECRUITMENT_NOTIFY_EMAIL],
            fail_silently=True,
        )

        return redirect("recruitment:thanks")

class CareerThanksView(TemplateView):
    template_name = "recruitment/thanks.html"