from typing import Any, Optional
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views import View
from django.views.generic import ListView, DetailView  # new
from django.views.generic.edit import FormView,CreateView, DeleteView, UpdateView
from .forms import AddUserForm,AssignRoleForm
from .models import Repository,Repo_role,Repo_user
from django.contrib.auth.models import User
from task.models import Task,Task_assignment
from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse

#repository views

class RepositoryListView(ListView):
    model = Repository
    template_name = "repository/repository_list.html"
    context_object_name = "repo_list"
    
    def get_queryset(self):
        return Repository.objects.all().filter(repo_id__in = Repo_user.objects.all().filter(username=self.request.user).values("role_id__repo_id").distinct())

    def get(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
        # If the user is not logged in, redirect to signup page.
        if not request.user.is_authenticated:
            return redirect("home")
            # return redirect("signup")
        return super().get(request, *args, **kwargs)
    
class CreateRepositoryView(CreateView):
    model = Repository
    fields = ["name"]
    template_name = "repository/repository_new.html"
    context_object_name = "repository"
    
    def get_success_url(self):
        return reverse("repo_detail", kwargs={"pk": self.object.repo_id , "name": self.object.name})
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user if user else None
        self.object = form.save()
        
        new_superadmin_role = Repo_role(
            role_name="Superadmin",
            can_change_status_if_task_assigned=True,
            can_manage_task=True,
            can_manage_users=True,
            can_manage_roles=True,
            can_cancel_repo=True,
            role_priority=0,
            repo_id=self.object
        )
        new_user_role = Repo_role(
            role_name="User",
            can_change_status_if_task_assigned=True,
            can_manage_task=False,
            can_manage_users=False,
            can_manage_roles=False,
            can_cancel_repo=False,
            role_priority=99,
            repo_id=self.object
        )
        new_superadmin_role.save()
        new_user_role.save()

        new_repo_user = Repo_user(username=user, role_id=new_superadmin_role)
        new_repo_user.save()
        
        return super(CreateRepositoryView, self).form_valid(form)
    
class RepositoryDetailView(DetailView):
    model = Repository
    template_name = "repository/repository_detail.html"
    context_object_name = "repo"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the tasks
        context["Repo_tasks"] = Task.objects.all().filter(repo_id = self.kwargs["pk"])
        context["Repo_tasks_assignment"] = Task_assignment.objects.all().filter(task_id__repo_id = self.kwargs["pk"])
        return context
    
class DeleteRepositoryView(DeleteView):
    model = Repository
    template_name = 'repository/repository_delete.html'

    def get_success_url(self):
        return reverse('repo_list')
    
#repo personal profile
class PersonalProfileView(DetailView):
    model = User
    template_name = "repository/repository_personal_profile.html"
    context_object_name = "Repo"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the tasks
        context["User_roles"] = Repo_user.objects.all().filter(username = self.request.user)
        context["User_tasks"] = Task_assignment.objects.all().filter(username = self.request.user)
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
    
class AssignRoleView(CreateView):
    form_class = AssignRoleForm
    template_name = "repository/role/role_assign.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["repo_id"] = self.kwargs["pk"]
        return kwargs
    
    def get_success_url(self):
        return reverse("role_list", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})

class RemoveAssignRoleView(DeleteView):
    model = Repo_user
    template_name = "repository/role/role_remove_assign.html"

    def get_success_url(self):
        return reverse("role_list", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def get_object(self):
        return Repo_user.objects.all().filter(username__username=self.kwargs["user"]).get(role_id=self.kwargs["role_id"])


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

class RemoveUserView(DeleteView):
    model = Repo_user
    template_name = "repository/repo_user/repo_user_remove.html"
    
    def get_success_url(self):
        return reverse("repo_user_list", kwargs={"pk": self.kwargs["pk"] , "name": self.kwargs["name"]})
    
    def get_object(self):
        return Repo_user.objects.all().filter(role_id__repo_id=self.kwargs["pk"]).filter(username__username=self.kwargs["user"])