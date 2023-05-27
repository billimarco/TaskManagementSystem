from django import forms
from .models import Task_assignment,Task
from repository.models import Repo_user
from django.contrib.auth.models import User
       
class AssignTaskForm(forms.ModelForm):
    class Meta:
       model = Task_assignment
       fields = ["username",
                 "task_id"]

    def __init__(self, *args, **kwargs):
       repo_id = kwargs.pop("repo_id", None)
       super().__init__(*args, **kwargs)
       self.fields["username"].queryset = User.objects.all().filter(username__in = Repo_user.objects.all().filter(role_id__repo_id = repo_id).values("username__username"))
       self.fields["task_id"].queryset = Task.objects.all().filter(repo_id = repo_id)