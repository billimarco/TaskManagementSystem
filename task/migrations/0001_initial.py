# Generated by Django 4.2.1 on 2023-05-24 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('N', 'New'), ('O', 'Ongoing'), ('W', 'Waiting'), ('F', 'Finished'), ('R', 'Removed')], default='N', max_length=1)),
                ('priority', models.CharField(choices=[('D', 'Deferable'), ('M', 'Moderate'), ('U', 'Urgent')], default='D', max_length=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('repo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.repository')),
            ],
            options={
                'db_table': 'tms_task',
            },
        ),
        migrations.CreateModel(
            name='Task_assignament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tms_task_assignament',
            },
        ),
    ]
