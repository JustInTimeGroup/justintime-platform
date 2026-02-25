from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import TrainingRegistrationForm
from .models import Training, TrainingRegistration


class PublishedTrainingMixin:
    def get_queryset(self):
        qs = Training.objects.all()
        qs = qs.filter(status=Training.Status.PUBLISHED)
        if hasattr(Training, "published_at"):
            qs = qs.filter(published_at__isnull=True) | qs.filter(published_at__lte=timezone.now())
        return qs.order_by("-start_date", "-published_at", "-created_at", "-id")


class TrainingListView(PublishedTrainingMixin, ListView):
    template_name = "training/list.html"
    context_object_name = "trainings"
    paginate_by = 10


class TrainingDetailView(PublishedTrainingMixin, DetailView):
    template_name = "training/detail.html"
    context_object_name = "training"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class TrainingApplyView(FormView):
    template_name = "training/register.html"
    form_class = TrainingRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        self.training = get_object_or_404(
            Training,
            slug=kwargs["slug"],
            status=Training.Status.PUBLISHED,
        )
        if self.training.published_at and self.training.published_at > timezone.now():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["training"] = self.training
        return ctx

    def form_valid(self, form):
        reg: TrainingRegistration = form.save(commit=False)
        reg.training = self.training

        # Unique per training/email (model constraint). If duplicate, show friendly error.
        try:
            reg.save()
        except Exception:
            form.add_error("email", "You are already registered for this training using this email.")
            return self.form_invalid(form)

        # Notify internal
        notify_to = getattr(settings, "TRAINING_NOTIFY_EMAIL", None)
        if notify_to:
            subject = f"New training registration: {self.training.title}"
            message = (
                f"New registration received.\n\n"
                f"Training: {self.training.title}\n"
                f"Name: {reg.full_name}\n"
                f"Email: {reg.email}\n"
                f"Phone: {reg.phone or '-'}\n"
                f"Organisation: {reg.organisation or '-'}\n\n"
                f"View in admin: /admin/training/trainingregistration/\n"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notify_to],
                fail_silently=True,
            )

        # Optional confirmation to registrant (enabled by default in dev)
        send_mail(
            subject=f"Registration received: {self.training.title}",
            message=(
                f"Hi {reg.full_name},\n\n"
                f"Thanks for registering for: {self.training.title}.\n"
                f"We’ll contact you with next steps.\n\n"
                f"Justintime Group"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reg.email],
            fail_silently=True,
        )

        return redirect("training:thanks")


class TrainingThanksView(TemplateView):
    template_name = "training/thanks.html"