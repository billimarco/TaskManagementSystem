from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from task.models import Task

class Repository(models.Model):
    repo_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_repository'
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        last_modified_task = Task.objects.filter(repo_id=self).order_by('-last_modified').first()
        if last_modified_task:
            self.last_modified = last_modified_task.last_modified
            super().save(*args, **kwargs)
        
class Repo_role(Group):
    role_id = models.AutoField(primary_key=True)
    repo_id = models.ForeignKey("Repository",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_repo_role'
        
    def __str__(self):
        try:
            return self.name.split('#')[0]
        except:
            return self.name
        
    @property
    def role_name(self):
        try:
            return self.name.split('#')[0]
        except:
            return self.name
        
class Repo_user(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    role_id = models.ForeignKey("Repo_role",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_repo_user'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'role_id'], name='unique_un_role_constraint'
            )
        ]
        