from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group


def ensure_default_groups():
    for name in ["member", "trainer", "manager"]:
        Group.objects.get_or_create(name=name)


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (u.is_staff or u.groups.filter(name="manager").exists())


class TrainerOrManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (
            u.is_staff or u.groups.filter(name__in=["trainer", "manager"]).exists()
        )
