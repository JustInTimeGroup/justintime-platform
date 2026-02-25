from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from apps.blog.models import Post
from apps.leads.models import Lead
from apps.recruitment.models import Job, JobApplication
from apps.training.models import Training, TrainingRegistration


# Role → which models the role can fully manage
ROLE_GROUPS = {
    "admin": {
        "models": [Post, Lead, Job, JobApplication, Training, TrainingRegistration],
        "full_access": True,
    },
    "marketing": {
        "models": [Post, Lead],
        "full_access": True,
    },
    "recruitment": {
        "models": [Job, JobApplication],
        "full_access": True,
    },
    "training": {
        "models": [Training, TrainingRegistration],
        "full_access": True,
    },
    "staff": {
        "models": [],
        "full_access": False,
    },
}


def _all_model_permissions(model_cls):
    """
    Returns all permissions for the given model (add/change/delete/view),
    using ContentType.
    """
    ct = ContentType.objects.get_for_model(model_cls)
    return Permission.objects.filter(content_type=ct)


@receiver(post_migrate)
def seed_role_groups(sender, app_config=None, **kwargs):
    """
    Seed/refresh role groups after migrations.

    Important: This runs after every app migration.
    We only execute on the accounts app migration to avoid extra work/noise.
    """
    if not app_config or app_config.label != "accounts":
        return

    for group_name, cfg in ROLE_GROUPS.items():
        group, _ = Group.objects.get_or_create(name=group_name)

        if not cfg["full_access"]:
            # Keep staff with no model permissions
            group.permissions.clear()
            continue

        perms = []
        for model in cfg["models"]:
            perms.extend(list(_all_model_permissions(model)))

        group.permissions.set(perms)