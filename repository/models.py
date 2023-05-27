from django.db import models
from django.conf import settings
from django.urls import reverse

class Repository(models.Model):
    repo_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_repository'
        
class Repo_role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=30)
    can_change_status_if_task_assigned = models.BooleanField(default=True)
    can_manage_task = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)
    can_manage_roles = models.BooleanField(default=False)
    can_cancel_repo = models.BooleanField(default=False)
    role_priority = models.IntegerField()
    repo_id = models.ForeignKey("Repository",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_repo_role'
        
class Repo_user(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    role_id = models.ForeignKey(Repo_role,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_repo_user'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'role_id'], name='unique_un_role_constraint'
            )
        ]
        