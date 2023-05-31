from django.contrib.auth.mixins import UserPassesTestMixin
from repository.models import Repo_user

class RepoRolePermissionRequiredMixin(UserPassesTestMixin):
    required_permissions = []

    def test_func(self):
        user = self.request.user
        repo_id = self.kwargs.get('repo_id')
        # Add your logic to retrieve the user's roles and check permissions
        user_roles = Repo_user.objects.filter(rp_user=user, role__repo_id=repo_id)
        required_perms = set(self.required_permissions)
        user_permissions = set()

        for role in user_roles:
            if role.role.can_change_status_if_task_assigned and 'can_change_status_if_task_assigned' not in user_permissions:
                user_permissions.add('can_change_status_if_task_assigned')
            if role.role.can_manage_tasks and 'can_manage_tasks' not in user_permissions:
                user_permissions.add('can_manage_tasks')
            if role.role.can_manage_users and 'can_manage_users' not in user_permissions:
                user_permissions.add('can_manage_users')
            if role.role.can_manage_roles and 'can_manage_roles' not in user_permissions:
                user_permissions.add('can_manage_roles')
            if role.role.can_cancel_repo and 'can_cancel_repo' not in user_permissions:
                user_permissions.add('can_cancel_repo')
            # Add more checks for other "can" fields as needed

        return required_perms.issubset(user_permissions)