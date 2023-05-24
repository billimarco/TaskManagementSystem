from django.urls import path
from . import views

urlpatterns = [
    path("assignedTasks/", views.AssignedTasksListView.as_view(), name="list_assigned_tasks"),
]