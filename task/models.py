from django.db import models
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    class Task_status(models.TextChoices):
        NEW = "N", _("New")
        ONGOING = "O", _("Ongoing")
        WAITING = "W", _("Waiting")
        FINISHED = "F", _("Finished")
        REMOVED = "R", _("Removed")

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,choices=Task_status.choices,default=Task_status.NEW)
    created_by = models.ForeignKey("user.User",on_delete=models.CASCADE)
    repo_id = models.ForeignKey("repository.Repository",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_task'
        
class Task_assignament(models.Model):
    task_id = models.ForeignKey("Task",on_delete=models.CASCADE)
    username = models.ForeignKey("user.User",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_task_assignament'