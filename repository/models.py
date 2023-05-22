from django.db import models

class Repository(models.Model):
    repo_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("User",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_repository'
        
class Repo_role(models.Model):
    role_id = models.PositiveSmallIntegerField(primary_key=True)
    role_name = models.CharField(max_length=30)
    manageTask_permission = models.BooleanField()
    manageUser_permission = models.BooleanField()
    manageUserRole_permission = models.BooleanField()
    role_priority = models.PositiveSmallIntegerField()
    
    class Meta:
        db_table = 'tms_repo_role'

class Repo_user(models.Model):
    repo_id = models.ForeignKey("Repository",on_delete=models.CASCADE)
    username = models.ForeignKey("user.User",on_delete=models.CASCADE)
    role_id = models.ForeignKey("Repo_role",on_delete=models.SET_DEFAULT)
    
    class Meta:
        db_table = 'tms_repo_user'
        