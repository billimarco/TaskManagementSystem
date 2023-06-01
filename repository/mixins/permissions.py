from django.contrib.auth.mixins import UserPassesTestMixin
from repository.models import Repo_user
from repository.utils import get_user_permissions

class RepoRolePermissionRequiredMixin(UserPassesTestMixin):
    required_permissions = []

    def test_func(self):
        user = self.request.user
        repo_id = self.kwargs.get('repo_id')
        # Add your logic to retrieve the user's roles and check permissions
        user_roles = Repo_user.objects.filter(rp_user=user, role__repo_id=repo_id)
        required_perms = set(self.required_permissions)
        user_permissions = get_user_permissions(user_roles)

        return required_perms.issubset(user_permissions)