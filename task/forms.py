from django import forms
from .models import Task_assignment,Task
from repository.models import Repo_user
from django.contrib.auth.models import User
       
class AssignTaskForm(forms.ModelForm):
    class Meta:
       model = Task_assignment
       fields = ["ass_user"]

    def __init__(self, *args, **kwargs):
       repo_id = kwargs.pop("repo_id", None)
       task_id = kwargs.pop("task_id", None)
       super().__init__(*args, **kwargs)
       usersInRepo = User.objects.all().filter(username__in = Repo_user.objects.all().filter(role__repo_id = repo_id).values("rp_user__username"))
       self.fields["ass_user"].queryset = usersInRepo.exclude(username__in = Task_assignment.objects.all().filter(task__task_id = task_id).values("ass_user__username"))