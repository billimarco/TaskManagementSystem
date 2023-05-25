from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.RepositoryListView.as_view(), name="repository_list"),
    path("<int:pk>_<str:name>/", views.RepositoryDetailView.as_view(), name="repository_detail"),
    path("<int:pk>_<str:name>/tasks/", include("task.urls")),
    path("<int:pk>_<str:name>/roles/", views.RolesListView.as_view(), name="role_list"),
    path("<int:pk>_<str:name>/roles/new/", views.CreateRoleView.as_view(), name="role_new"),
    path("<int:pk>_<str:name>/roles/<int:role_id>/edit/", views.ModifyRoleView.as_view(), name="role_edit"),
    path("<int:pk>_<str:name>/roles/<int:role_id>/delete/", views.DeleteRoleView.as_view(), name="role_delete")
    #path("<int:pk>_<str:name>/roles/assign/",views.TaskDetailView.as_view(), name="role_assign"),
    #path("<int:pk>_<str:name>/delete/",views.TaskDetailView.as_view(), name="repo_delete"),
    #path("new/",views.TaskDetailView.as_view(), name="repo_new"),
    #path("<int:pk>_<str:name>/adduser/",views.TaskDetailView.as_view(), name="repo_add_user"),
    #path("<int:pk>_<str:name>/profile_<str:username>/",views.TaskDetailView.as_view(), name="repo_personal_profile"),
]