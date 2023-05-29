from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.CreateTaskView.as_view(), name="task_new"),
    path("<int:task_id>/",views.TaskDetailView.as_view(), name="task_detail"),
    path("<int:task_id>/assign/", views.AssignTaskView.as_view(), name="task_assign"),
    path("<int:task_id>/edit/", views.ModifyTaskView.as_view(), name="task_edit"),
    path("<int:task_id>/status/", views.ModifyTaskStatusView.as_view(), name="task_status"),
    path("<int:task_id>/delete/", views.DeleteTaskView.as_view(), name="task_delete"),
    path("<int:task_id>/history/", views.HistoryTaskView.as_view(), name="task_history"),
    path("<int:task_id>_<str:task_title>_<str:username>/remove_assign/",views.RemoveAssignTaskView.as_view(), name="task_remove_assign"),
]