from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


GROUP_PERM_MAP = {
    "member": [],
    "trainer": [
        "view_client",
        "change_client",
        "add_client",
        "view_program",
        "change_program",
        "add_program",
        "view_review",
        "add_review",
    ],
    "manager": [
        "view_client",
        "change_client",
        "add_client",
        "delete_client",
        "view_program",
        "change_program",
        "add_program",
        "delete_program",
        "view_membershipplan",
        "change_membershipplan",
        "add_membershipplan",
        "delete_membershipplan",
        "view_subscription",
        "change_subscription",
        "add_subscription",
        "delete_subscription",
        "view_review",
        "add_review",
        "change_review",
    ],
}


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    for group_name, codenames in GROUP_PERM_MAP.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        if not codenames:
            continue
        perms = Permission.objects.filter(codename__in=codenames)
        group.permissions.add(*perms)
