from django.views.generic import ListView, DetailView  # new
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import AssignTaskForm
from .models import Task,Task_assignment,Task_status_history
from repository.mixins.permissions import RepoRolePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from repository.models import Repository,Repo_role,Repo_user
from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse

    
class AssignedTasksListView(LoginRequiredMixin,ListView):
    model = Task_assignment
    template_name = "list_assigned_tasks.html"
    context_object_name = "user_task_list"
    pk_url_kwarg = "repo_id"
    
    def get_queryset(self):
        return Task_assignment.objects.all().filter(ass_user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repo_auth_user_role"] = Repo_user.objects.all().filter(rp_user=self.request.user)
        return context
    
class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    template_name = "repository/task/task_detail.html"
    context_object_name = "task"
    pk_url_kwarg = "repo_id"
    
    def get_object(self):
        return Task.objects.get(task_id=self.kwargs["task_id"])
    
#Repo_tasks feature
    
class CreateTaskView(LoginRequiredMixin,RepoRolePermissionRequiredMixin,CreateView):
    model = Task
    fields = ["title",
              "description",
              "priority"]
    template_name = "repository/task/task_new.html"
    context_object_name = "task"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_tasks"]
    
    def get_success_url(self):
        return reverse("repo_detail", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.status = "N"
        form.instance.created_by = user if user else None
        form.instance.repo = Repository.objects.get(repo_id=self.kwargs["repo_id"])
        return super(CreateTaskView, self).form_valid(form)

class AssignTaskView(LoginRequiredMixin,RepoRolePermissionRequiredMixin,CreateView):
    form_class = AssignTaskForm
    template_name = "repository/task/task_assign.html"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_tasks"]
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["repo_id"] = self.kwargs["repo_id"]
        kwargs["task_id"] = self.kwargs["task_id"]
        return kwargs
    
    def get_success_url(self):
        return reverse("repo_detail", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def form_valid(self, form):
        form.instance.task = Task.objects.get(task_id=self.kwargs["task_id"])
        return super(AssignTaskView, self).form_valid(form)

class RemoveAssignTaskView(LoginRequiredMixin,RepoRolePermissionRequiredMixin,DeleteView):
    model = Task_assignment
    template_name = "repository/task/task_remove_assign.html"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_tasks"]

    def get_success_url(self):
        return reverse("repo_detail", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def get_object(self):
        return Task_assignment.objects.all().filter(ass_user__username=self.kwargs["username"]).get(task__task_id=self.kwargs["task_id"])
    
class ModifyTaskView(LoginRequiredMixin,RepoRolePermissionRequiredMixin,UpdateView):
    model = Task
    fields = ["title",
              "description",
              "status",
              "priority"]
    template_name = "repository/task/task_edit.html"
    context_object_name = "task"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_tasks"]
    
    def get_success_url(self):
        return reverse("repo_detail", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def get_object(self):
        return Task.objects.get(task_id=self.kwargs["task_id"])
    
class ModifyTaskStatusView(LoginRequiredMixin,RepoRolePermissionRequiredMixin,UpdateView):
    model = Task
    fields = ["status"]
    template_name = "repository/task/task_edit.html"
    context_object_name = "task"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_change_status_if_task_assigned"]
    
    def get_success_url(self):
        return reverse("repo_detail", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def get_object(self):
        return Task.objects.get(task_id=self.kwargs["task_id"])
    
class DeleteTaskView(LoginRequiredMixin,RepoRolePermissionRequiredMixin,DeleteView):
    model = Task
    template_name = "repository/task/task_delete.html"
    context_object_name = "task"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_tasks"]
    
    def get_success_url(self):
        return reverse("repo_detail", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def get_object(self):
        return Task.objects.get(task_id=self.kwargs["task_id"])
    
class HistoryTaskView(LoginRequiredMixin,ListView):
    model = Task_status_history
    template_name = "repository/task/task_history.html"
    context_object_name = "history_list"
    pk_url_kwarg = "repo_id"

    def get_queryset(self):
        task_id = self.kwargs["task_id"]
        return Task_status_history.objects.filter(task__task_id=task_id).order_by("-created")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = Task.objects.get(task_id = self.kwargs["task_id"])
        return context