# Generated by Django 4.2.1 on 2023-05-28 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_alter_task_status_history_task_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task_status_history',
            old_name='task_id',
            new_name='task',
        ),
    ]
