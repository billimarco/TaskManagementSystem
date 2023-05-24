from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views import View
from django.views.generic import ListView, DetailView  # new
from task.models import Task,Task_assignament
from django.shortcuts import redirect

    
class AssignedTasksListView(ListView):
    model = Task_assignament
    template_name = "list_assigned_tasks.html"
    
    def get_queryset(self):
        return Task_assignament.objects.all().filter(username__exact=self.request.user)

    def get(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
        # If the user is not logged in, redirect to signup page.
        if not request.user.is_authenticated:
            return redirect("home")
            # return redirect("signup")
        return super().get(request, *args, **kwargs)
