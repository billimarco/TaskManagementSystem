# Generated by Django 4.2.1 on 2023-05-27 11:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Task_assignament',
            new_name='Task_assignment',
        ),
        migrations.AddConstraint(
            model_name='task_assignment',
            constraint=models.UniqueConstraint(fields=('username', 'task_id'), name='unique_un_task_constraint'),
        ),
    ]
