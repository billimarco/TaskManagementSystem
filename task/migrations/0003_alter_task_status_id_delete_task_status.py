# Generated by Django 4.2.1 on 2023-05-23 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_rename_status_task_status_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status_id',
            field=models.CharField(choices=[('N', 'New'), ('O', 'Ongoing'), ('W', 'Waiting'), ('F', 'Finished'), ('R', 'Removed')], default='N', max_length=1),
        ),
        migrations.DeleteModel(
            name='Task_status',
        ),
    ]
