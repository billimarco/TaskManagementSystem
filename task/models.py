from django.db import models

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",on_delete=models.CASCADE)
    status = models.ForeignKey("Task_status",on_delete=models.CASCADE)
    repo_id = models.ForeignKey("repository.Repository",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_task'

class Task_status(models.Model):
    status_id = models.PositiveSmallIntegerField(primary_key=True)
    status_name = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'tms_task_status'
        
class Task_assignament(models.Model):
    task_id = models.ForeignKey("Task",on_delete=models.CASCADE)
    username = models.ForeignKey("user.User",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_task_assignament'