# Generated by Django 4.2.1 on 2023-05-23 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_task_status_id_delete_task_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='status_id',
            new_name='status',
        ),
    ]
