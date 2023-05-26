from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views import View
from django.views.generic import ListView, DetailView  # new
from django.views.generic.edit import FormView,CreateView, DeleteView, UpdateView
from .forms import AddUserForm
from .models import Repository,Repo_role,Repo_user
from django.contrib.auth.models import User
from task.models import Task,Task_assignament
from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse

#repository views

class RepositoryListView(ListView):
    model = Repository
    template_name = "repository/list_repository.html"
    context_object_name = "repo_list"
    
    def get_queryset(self):
        return Repository.objects.all().filter(repo_id__in = Repo_user.objects.all().filter(username=self.request.user).values("role_id__repo_id").distinct())

    def get(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
        # If the user is not logged in, redirect to signup page.
        if not request.user.is_authenticated:
            return redirect("home")
            # return redirect("signup")
        return super().get(request, *args, **kwargs)
    
class RepositoryDetailView(DetailView):
    model = Repository
    template_name = "repository/repository_detail.html"
    context_object_name = "repo"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the tasks
        context["Repo_tasks"] = Task.objects.all().filter(repo_id = self.kwargs["pk"])
        return context
    

#roles views
    
class RolesListView(ListView):
    model = Repo_role
    template_name = "repository/role/role_list.html"
    context_object_name = "role_list"
    
    def get_queryset(self):
        return Repo_role.objects.all().filter(repo_id = self.kwargs["pk"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repo"] = Repository.objects.get(repo_id = self.kwargs["pk"])
        context["repo_users"] = Repo_user.objects.all().filter(role_id__repo_id=self.kwargs["pk"])
        return context

    def get(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
        # If the user is not logged in, redirect to signup page.
        if not request.user.is_authenticated:
            return redirect("home")
            # return redirect("signup")
        return super().get(request, *args, **kwargs)

class CreateRoleView(CreateView):
    model = Repo_role
    fields = ["role_name",
              "can_change_status_if_task_assigned",
              "can_manage_task",
              "can_manage_users",
              "can_manage_roles",
              "can_cancel_repo",
              "role_priority"]
    template_name = "repository/role/role_new.html"
    context_object_name = "role"
    
    def get_success_url(self):
        return reverse("role_list", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def form_valid(self, form):
        form.instance.repo_id = Repository.objects.get(repo_id=self.kwargs["pk"])
        return super(CreateRoleView, self).form_valid(form)

class ModifyRoleView(UpdateView):
    model = Repo_role
    fields = ["role_name",
              "can_change_status_if_task_assigned",
              "can_manage_task",
              "can_manage_users",
              "can_manage_roles",
              "can_cancel_repo",
              "role_priority"]
    template_name = "repository/role/role_edit.html"
    context_object_name = "role"
    
    def get_success_url(self):
        return reverse("role_list", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def get_object(self):
        return Repo_role.objects.get(role_id=self.kwargs["role_id"])

class DeleteRoleView(DeleteView):
    model = Repo_role
    template_name = "repository/role/role_delete.html"
    context_object_name = "role"
    
    def get_success_url(self):
        return reverse("role_list", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def get_object(self):
        return Repo_role.objects.get(role_id=self.kwargs["role_id"])


#repo_users views

   
class UsersListView(ListView):
    model = Repo_user
    template_name = "repository/repo_user/repo_user_list.html"
    context_object_name = "repo_user_list"
    
    def get_queryset(self):
        return Repo_user.objects.all().filter(role_id__repo_id=self.kwargs["pk"]).values("username__username").distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users_role_list"] = Repo_user.objects.all().filter(role_id__repo_id = self.kwargs["pk"])
        context["repo"] = Repository.objects.get(repo_id = self.kwargs["pk"])
        return context

    def get(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
        # If the user is not logged in, redirect to signup page.
        if not request.user.is_authenticated:
            return redirect("home")
            # return redirect("signup")
        return super().get(request, *args, **kwargs)

class AddUserView(CreateView):
    form_class = AddUserForm
    template_name = "repository/repo_user/repo_user_add.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["repo_id"] = self.kwargs["pk"]
        return kwargs
    
    def get_success_url(self):
        return reverse("repo_user_list", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})

class AssignRoleToUserView(UpdateView):
    model = Repo_user
    fields = ["role_name",
              "can_change_status_if_task_assigned",
              "can_manage_task",
              "can_assign_task",
              "can_add_people",
              "can_manage_roles",
              "can_cancel_repo",
              "role_priority"]
    template_name = "repository/repo_user/repo_user_assign_role.html"
    context_object_name = "role"
    
    def get_success_url(self):
        return reverse("repo_user_list", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def get_object(self):
        return Repo_role.objects.get(role_name=self.kwargs["role_name"])

class RemoveUserView(DeleteView):
    model = Repo_user
    template_name = "repository/repo_user/repo_user_remove.html"
    
    def get_success_url(self):
        return reverse("repo_user_list", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repo_user"] = User.objects.get(username=self.kwargs["username"])
        return context
    
    def get_object(self):
        return Repo_user.objects.all().filter(role_id__repo_id=self.kwargs["pk"]).filter(username__username=self.kwargs["username"])