from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.RepositoryListView.as_view(), name="repo_list"),
    path("new/",views.CreateRepositoryView.as_view(), name="repo_new"),
    path("<int:repo_id>_<str:repo_name>/", views.RepositoryDetailView.as_view(), name="repo_detail"),
    path("<int:repo_id>_<str:repo_name>/delete/",views.DeleteRepositoryView.as_view(), name="repo_delete"),
    path("<int:repo_id>_<str:repo_name>/profile_<str:username>/",views.PersonalProfileView.as_view(), name="repo_personal_profile"),
    path("<int:repo_id>_<str:repo_name>/tasks/", include("task.urls")),
    path("<int:repo_id>_<str:repo_name>/roles/", views.RolesListView.as_view(), name="role_list"),
    path("<int:repo_id>_<str:repo_name>/roles/new/", views.CreateRoleView.as_view(), name="role_new"),
    path("<int:repo_id>_<str:repo_name>/roles/<int:role_id>/assign/",views.AssignRoleView.as_view(), name="role_assign"),
    path("<int:repo_id>_<str:repo_name>/roles/<int:role_id>/edit/", views.ModifyRoleView.as_view(), name="role_edit"),
    path("<int:repo_id>_<str:repo_name>/roles/<int:role_id>/delete/", views.DeleteRoleView.as_view(), name="role_delete"),
    path("<int:repo_id>_<str:repo_name>/roles/<int:role_id>_<str:role_name>_<str:username>/remove_assign/",views.RemoveAssignRoleView.as_view(), name="role_remove_assign"),
    path("<int:repo_id>_<str:repo_name>/users/",views.UsersListView.as_view(), name="repo_user_list"),
    path("<int:repo_id>_<str:repo_name>/users/add_user/", views.AddUserView.as_view(), name="repo_user_add"),
    path("<int:repo_id>_<str:repo_name>/users/<str:username>/remove_user/", views.RemoveUserView.as_view(), name="repo_user_remove"),
]