from typing import Any, Dict, Optional
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views import View
from django.views.generic import ListView, DetailView  # new
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import AssignTaskForm
from repository.models import Repository,Repo_role
from .models import Task,Task_assignment
from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse

    
class AssignedTasksListView(ListView):
    model = Task_assignment
    template_name = "list_assigned_tasks.html"
    context_object_name = "task_list"
    
    def get_queryset(self):
        return Task_assignment.objects.all().filter(username__exact=self.request.user)

    def get(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
        # If the user is not logged in, redirect to signup page.
        if not request.user.is_authenticated:
            return redirect("home")
            # return redirect("signup")
        return super().get(request, *args, **kwargs)
    
class TaskDetailView(DetailView):
    model = Task
    template_name = "repository/task/task_detail.html"
    context_object_name = "task"
    
    def get_object(self):
        return Task.objects.get(task_id=self.kwargs["task_pk"])
    
class CreateTaskView(CreateView):
    model = Task
    fields = ["title",
              "description",
              "priority"]
    template_name = "repository/task/task_new.html"
    context_object_name = "task"
    
    def get_success_url(self):
        return reverse("repository_detail", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.status = "N"
        form.instance.created_by = user if user else None
        form.instance.repo_id = Repository.objects.get(repo_id=self.kwargs["pk"])
        return super(CreateTaskView, self).form_valid(form)

class ModifyTaskView(UpdateView):
    model = Task
    fields = ["title",
              "description",
              "status",
              "priority"]
    template_name = "repository/task/task_edit.html"
    context_object_name = "task"
    
    def get_success_url(self):
        return reverse("repository_detail", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def get_object(self):
        return Task.objects.get(task_id=self.kwargs["task_pk"])

class DeleteTaskView(DeleteView):
    model = Task
    template_name = "repository/task/task_delete.html"
    context_object_name = "task"
    
    def get_success_url(self):
        return reverse("repository_detail", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def get_object(self):
        return Task.objects.get(task_id=self.kwargs["task_pk"])
    
class ModifyTaskStatusView(UpdateView):
    model = Task
    fields = ["status"]
    template_name = "repository/task/task_edit.html"
    context_object_name = "task"
    
    def get_success_url(self):
        return reverse("repository_detail", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def get_object(self):
        return Task.objects.get(task_id=self.kwargs["task_pk"])

class AssignTaskView(CreateView):
    form_class = AssignTaskForm
    template_name = "repository/task/task_assign.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["repo_id"] = self.kwargs["pk"]
        return kwargs
    
    def get_success_url(self):
        return reverse("repository_detail", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
