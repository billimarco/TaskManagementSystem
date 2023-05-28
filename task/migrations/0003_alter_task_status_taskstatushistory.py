# Generated by Django 4.2.1 on 2023-05-28 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_rename_task_assignament_task_assignment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('N', 'New'), ('O', 'Ongoing'), ('W', 'Waiting'), ('F', 'Finished')], default='N', max_length=1),
        ),
        migrations.CreateModel(
            name='TaskStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('N', 'New'), ('O', 'Ongoing'), ('W', 'Waiting'), ('F', 'Finished')], max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
            ],
            options={
                'db_table': 'tms_task_status_history',
            },
        ),
    ]