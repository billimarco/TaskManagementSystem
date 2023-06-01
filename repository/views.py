from django.http import HttpResponse
from django.http import HttpRequest
from django.views.generic import ListView, DetailView  # new
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .mixins.permissions import RepoRolePermissionRequiredMixin
from .forms import AddUserForm,AssignRoleForm
from .models import Repository,Repo_role,Repo_user
from task.models import Task,Task_assignment
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse

#repository views

class RepositoryListView(ListView):
    model = Repository
    template_name = "repository/repository_list.html"
    context_object_name = "repo_list"
    pk_url_kwarg = "repo_id"
    
    def get_queryset(self):
        return Repository.objects.all().filter(repo_id__in = Repo_user.objects.all().filter(rp_user=self.request.user).values("role__repo_id").distinct())

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
    pk_url_kwarg = "repo_id"
    
    def get_success_url(self):
        return reverse("repo_detail", kwargs={"repo_id": self.object.repo_id , "repo_name": self.object.name})
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user if user else None
        self.object = form.save()
        
        new_superadmin_role = Repo_role(
            role_name="Superadmin",
            can_change_status_if_task_assigned=True,
            can_manage_tasks=True,
            can_manage_users=True,
            can_manage_roles=True,
            can_cancel_repo=True,
            repo=self.object
        )
        new_user_role = Repo_role(
            role_name="User",
            can_change_status_if_task_assigned=True,
            can_manage_tasks=False,
            can_manage_users=False,
            can_manage_roles=False,
            can_cancel_repo=False,
            repo=self.object
        )
        new_superadmin_role.save()
        new_user_role.save()

        new_repo_user = Repo_user(rp_user=user, role=new_superadmin_role)
        new_repo_user.save()
        
        return super(CreateRepositoryView, self).form_valid(form)
    
class RepositoryDetailView(DetailView):
    model = Repository
    template_name = "repository/repository_detail.html"
    context_object_name = "repository"
    pk_url_kwarg = "repo_id"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the tasks
        context["repo_tasks"] = Task.objects.all().filter(repo__repo_id = self.kwargs["repo_id"])
        context["repo_tasks_assignment"] = Task_assignment.objects.all().filter(task__repo__repo_id = self.kwargs["repo_id"])
        context["repo_auth_user_role"] = Repo_user.objects.all().filter(rp_user=self.request.user).filter(role__repo__repo_id = self.kwargs["repo_id"])
        return context
    
class DeleteRepositoryView(RepoRolePermissionRequiredMixin,DeleteView):
    model = Repository
    template_name = 'repository/repository_delete.html'
    pk_url_kwarg = "repo_id"
    required_permissions = ["can_cancel_repo"]

    def get_success_url(self):
        return reverse('repo_list')
    
#repo personal profile
class PersonalProfileView(DetailView):
    model = User
    template_name = "repository/repository_personal_profile.html"
    pk_url_kwarg = "repo_id"
    
    def get_object(self):
        return User.objects.all().filter(username = self.kwargs["username"])
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the tasks
        context["user_roles"] = Repo_user.objects.all().filter(rp_user__username = self.kwargs["username"]).filter(role__repo__repo_id = self.kwargs["repo_id"])
        context["user_tasks"] = Task_assignment.objects.all().filter(ass_user__username = self.kwargs["username"]).filter(task__repo__repo_id = self.kwargs["repo_id"])
        context["repo_tasks_assignment"] = Task_assignment.objects.all().filter(task__repo__repo_id = self.kwargs["repo_id"])
        context["repo_auth_user_role"] = Repo_user.objects.all().filter(rp_user=self.request.user).filter(role__repo__repo_id = self.kwargs["repo_id"])
        return context
    

#roles views
    
class RolesListView(RepoRolePermissionRequiredMixin,ListView):
    model = Repo_role
    template_name = "repository/role/role_list.html"
    context_object_name = "role_list"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_roles"]
    
    def get_queryset(self):
        return Repo_role.objects.all().filter(repo__repo_id = self.kwargs["repo_id"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repo"] = Repository.objects.get(repo_id = self.kwargs["repo_id"])
        context["repo_users"] = Repo_user.objects.all().filter(role__repo__repo_id=self.kwargs["repo_id"])
        return context

    def get(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
        # If the user is not logged in, redirect to signup page.
        if not request.user.is_authenticated:
            return redirect("home")
            # return redirect("signup")
        return super().get(request, *args, **kwargs)

class CreateRoleView(RepoRolePermissionRequiredMixin,CreateView):
    model = Repo_role
    fields = ["role_name",
              "can_change_status_if_task_assigned",
              "can_manage_tasks",
              "can_manage_users",
              "can_manage_roles",
              "can_cancel_repo"]
    template_name = "repository/role/role_new.html"
    context_object_name = "role"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_roles"]
    
    def get_success_url(self):
        return reverse("role_list", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def form_valid(self, form):
        form.instance.repo = Repository.objects.get(repo_id=self.kwargs["repo_id"])
        return super(CreateRoleView, self).form_valid(form)

class ModifyRoleView(RepoRolePermissionRequiredMixin,UpdateView):
    model = Repo_role
    fields = ["role_name",
              "can_change_status_if_task_assigned",
              "can_manage_tasks",
              "can_manage_users",
              "can_manage_roles",
              "can_cancel_repo"]
    template_name = "repository/role/role_edit.html"
    context_object_name = "role"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_roles"]
    
    def get_success_url(self):
        return reverse("role_list", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def get_object(self):
        return Repo_role.objects.get(role_id=self.kwargs["role_id"])

class DeleteRoleView(RepoRolePermissionRequiredMixin,DeleteView):
    model = Repo_role
    template_name = "repository/role/role_delete.html"
    context_object_name = "role"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_roles"]
    
    def get_success_url(self):
        return reverse("role_list", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def get_object(self):
        return Repo_role.objects.get(role_id=self.kwargs["role_id"])
    
class AssignRoleView(RepoRolePermissionRequiredMixin,CreateView):
    form_class = AssignRoleForm
    template_name = "repository/role/role_assign.html"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_roles"]
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["repo_id"] = self.kwargs["repo_id"]
        kwargs["role_id"] = self.kwargs["role_id"]
        return kwargs
    
    def get_success_url(self):
        return reverse("role_list", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def form_valid(self, form):
        form.instance.role = Repo_role.objects.get(role_id=self.kwargs["role_id"])
        return super(AssignRoleView, self).form_valid(form)

class RemoveAssignRoleView(RepoRolePermissionRequiredMixin,DeleteView):
    model = Repo_user
    template_name = "repository/role/role_remove_assign.html"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_roles"]

    def get_success_url(self):
        return reverse("role_list", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def get_object(self):
        return Repo_user.objects.all().filter(rp_user__username=self.kwargs["username"]).get(role__role_id=self.kwargs["role_id"])


#repo_users views

   
class UsersListView(RepoRolePermissionRequiredMixin,ListView):
    model = Repo_user
    template_name = "repository/repo_user/repo_user_list.html"
    context_object_name = "repo_user_list"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_users"]
    
    def get_queryset(self):
        return User.objects.all().filter(username__in=Repo_user.objects.all().filter(role__repo__repo_id = self.kwargs["repo_id"]).values_list("rp_user__username", flat=True))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users_role_list"] = Repo_user.objects.all().filter(role__repo__repo_id = self.kwargs["repo_id"])
        context["repo"] = Repository.objects.get(repo_id = self.kwargs["repo_id"])
        return context

    def get(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
        # If the user is not logged in, redirect to signup page.
        if not request.user.is_authenticated:
            return redirect("home")
            # return redirect("signup")
        return super().get(request, *args, **kwargs)

class AddUserView(RepoRolePermissionRequiredMixin,CreateView):
    form_class = AddUserForm
    template_name = "repository/repo_user/repo_user_add.html"
    pk_url_kwarg = "repo_id"
    required_permissions=["can_manage_users"]
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["repo_id"] = self.kwargs["repo_id"]
        return kwargs
    
    def get_success_url(self):
        return reverse("repo_user_list", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})

class RemoveUserView(RepoRolePermissionRequiredMixin,DeleteView):
    model = Repo_user
    template_name = "repository/repo_user/repo_user_remove.html"
    required_permissions=["can_manage_users"]
    
    def get_success_url(self):
        return reverse("repo_user_list", kwargs={"repo_id": self.kwargs["repo_id"] , "repo_name": self.kwargs["repo_name"]})
    
    def get_object(self):
        return Repo_user.objects.all().filter(role__repo__repo_id=self.kwargs["repo_id"]).filter(rp_user__username=self.kwargs["username"])