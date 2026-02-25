from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.utils import timezone

from .models import Post


class PublishedPostQuerysetMixin:
    """
    Handles common enterprise pattern:
    - show only published posts
    - support either `is_published` boolean OR `status` choices
    - support either `published_at` datetime OR fallback to `created_at`
    """

    def get_queryset(self):
        qs = Post.objects.all()

        # --- Publication filter (adjust if your model differs) ---
        if hasattr(Post, "is_published"):
            qs = qs.filter(is_published=True)

        if hasattr(Post, "status"):
            # common values: "published", "draft"
            qs = qs.filter(status__iexact="published")

        # --- Publish date gate (optional) ---
        if hasattr(Post, "published_at"):
            qs = qs.filter(Q(published_at__isnull=True) | Q(published_at__lte=timezone.now()))
            qs = qs.order_by("-published_at", "-id")
        elif hasattr(Post, "created_at"):
            qs = qs.order_by("-created_at", "-id")
        else:
            qs = qs.order_by("-id")

        return qs


class BlogListView(PublishedPostQuerysetMixin, ListView):
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 8


class BlogDetailView(PublishedPostQuerysetMixin, DetailView):
    template_name = "blog/detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"