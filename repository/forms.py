from django import forms
from .models import Repo_user,Repo_role,Repository
from django.contrib.auth.models import User


class AddUserForm(forms.ModelForm):
    class Meta:
       model = Repo_user
       fields = ["username",
                "role_id"]

    def __init__(self, *args, **kwargs):
       repo_id = kwargs.pop('repo_id', None)
       super().__init__(*args, **kwargs)
       self.fields["username"].queryset = User.objects.all().exclude(username__in = Repo_user.objects.all().filter(role_id__repo_id = repo_id).values("username__username"))
       self.fields["role_id"].queryset = Repo_role.objects.all().filter(repo_id = repo_id)