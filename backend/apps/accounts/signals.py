from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from apps.blog.models import Post
from apps.leads.models import ContactLead, NewsletterSubscriber
from apps.recruitment.models import Job, JobApplication
from apps.training.models import Training, TrainingRegistration


ROLE_GROUPS = {
    "admin": {
        "models": [Post, ContactLead, NewsletterSubscriber, Job, JobApplication, Training, TrainingRegistration],
        "full_access": True,
    },
    "marketing": {
        "models": [Post, ContactLead, NewsletterSubscriber],
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


@receiver(post_migrate)
def seed_role_groups(sender, **kwargs):
    for group_name, cfg in ROLE_GROUPS.items():
        group, _ = Group.objects.get_or_create(name=group_name)

        if cfg["full_access"]:
            perms = []
            for model in cfg["models"]:
                ct = ContentType.objects.get_for_model(model)
                perms.extend(Permission.objects.filter(content_type=ct))
            group.permissions.set(perms)
