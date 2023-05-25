from django.urls import path
from . import views

urlpatterns = [
    path("<int:task_pk>/",views.TaskDetailView.as_view(), name="task_detail"),
    path("<int:task_pk>/edit/", views.ModifyTaskView.as_view(), name="task_edit"),
    path("<int:task_pk>/status/", views.ModifyTaskStatusView.as_view(), name="task_status"),
    path("<int:task_pk>/delete/", views.DeleteTaskView.as_view(), name="task_delete"),
    #path("<int:task_pk>/assign/", views.DeleteTaskView.as_view(), name="task_assign"),
    path("new/", views.CreateTaskView.as_view(), name="task_new"),
]