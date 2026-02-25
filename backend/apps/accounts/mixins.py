from django.contrib.auth.mixins import UserPassesTestMixin


class RoleRequiredMixin(UserPassesTestMixin):
    required_roles: tuple[str, ...] = ()

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if not self.required_roles:
            return True
        return getattr(user, "role", None) in self.required_roles
