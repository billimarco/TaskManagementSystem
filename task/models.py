from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Task(models.Model):
    class Task_status(models.TextChoices):
        NEW = "N", _("New")
        ONGOING = "O", _("Ongoing")
        WAITING = "W", _("Waiting")
        FINISHED = "F", _("Finished")
        
    class Task_priority(models.TextChoices):
        DEFERABLE = "D", _("Deferable")
        MODERATE = "M", _("Moderate")
        URGENT = "U", _("Urgent")

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,choices=Task_status.choices,default=Task_status.NEW)
    priority = models.CharField(max_length=1,choices=Task_priority.choices,default=Task_priority.DEFERABLE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    repo = models.ForeignKey("repository.Repository",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_task'
    
    def clean(self):
        if self.pk:
            original_status = Task.objects.values_list('status', flat=True).get(pk=self.pk)
            if original_status == "F":
                raise ValidationError("Cannot modify a finished task.")
            
    def save(self, *args, **kwargs):
        self.full_clean()
        is_new_task = not self.pk  # Check if the task is being created
        original_status = self._get_original_status()

        super().save(*args, **kwargs)

        if is_new_task or ((not is_new_task) and self.status != original_status):
            Task_status_history.objects.create(task=self, status=self.status)


    def _get_original_status(self):
        if self.pk:
            return Task.objects.filter(pk=self.pk).values_list('status', flat=True).first()
        return None
    
    def __str__(self):
        return f"{self.task_id} - {self.title} - {self.repo.name}"

@receiver(pre_save, sender=Task)
def update_last_modified(sender, instance, **kwargs):
    if instance.pk:  # Only update if the task already exists
        original_task = Task.objects.get(pk=instance.pk)
        if original_task.last_modified != instance.last_modified:
            # The last_modified attribute has changed
            repository = instance.repo
            repository.last_modified = instance.last_modified
            repository.save()
            
@receiver(post_save, sender=Task)
def update_repository_last_modified(sender, instance, **kwargs):
    repository = instance.repo
    if repository:
        last_modified_task = Task.objects.filter(repo=repository).order_by('-last_modified').first()
        if last_modified_task:
            repository.last_modified = last_modified_task.last_modified
            repository.save()
        
class Task_assignment(models.Model):
    ass_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    task = models.ForeignKey("Task",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tms_task_assignament'
        constraints = [
            models.UniqueConstraint(
                fields=['ass_user', 'task'], name='unique_un_task_constraint'
            )
        ]
        
    def __str__(self):
        return f"{self.task.task_id} - {self.ass_user.username}"

class Task_status_history(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=Task.Task_status.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tms_task_status_history'
        
    def __str__(self):
        return f"{self.task.task_id} - {self.created}"