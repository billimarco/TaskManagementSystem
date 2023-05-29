from django import forms
from .models import Repo_user,Repo_role,Repository
from django.contrib.auth.models import User


class AddUserForm(forms.ModelForm):
    class Meta:
       model = Repo_user
       fields = ["rp_user",
                "role"]

    def __init__(self, *args, **kwargs):
       repo_id = kwargs.pop("repo_id", None)
       super().__init__(*args, **kwargs)
       self.fields["rp_user"].queryset = User.objects.all().exclude(username__in = Repo_user.objects.all().filter(role__repo_id = repo_id).values("rp_user__username"))
       self.fields["role"].queryset = Repo_role.objects.all().filter(repo__repo_id = repo_id)
       
class AssignRoleForm(forms.ModelForm):
    class Meta:
       model = Repo_user
       fields = ["rp_user"]

    def __init__(self, *args, **kwargs):
       repo_id = kwargs.pop("repo_id", None)
       role_id = kwargs.pop("role_id", None)
       super().__init__(*args, **kwargs)
       usersInRepo = User.objects.all().filter(username__in = Repo_user.objects.all().filter(role__repo_id = repo_id).values("rp_user__username"))
       self.fields["rp_user"].queryset = usersInRepo.exclude(username__in = Repo_role.objects.all().filter(role_id = role_id).values("repo_user__rp_user__username"))