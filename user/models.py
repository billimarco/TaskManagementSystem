from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'tms_user'
