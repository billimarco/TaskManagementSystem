# Generated by Django 4.2.1 on 2023-05-25 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('repo_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tms_repository',
            },
        ),
        migrations.CreateModel(
            name='Repo_role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=30)),
                ('can_change_status_if_task_assigned', models.BooleanField(default=True)),
                ('can_manage_task', models.BooleanField(default=False)),
                ('can_assign_task', models.BooleanField(default=False)),
                ('can_add_people', models.BooleanField(default=False)),
                ('can_manage_roles', models.BooleanField(default=False)),
                ('can_cancel_repo', models.BooleanField(default=False)),
                ('role_priority', models.IntegerField()),
                ('repo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.repository')),
                ('repo_users', models.ManyToManyField(db_table='tms_repo_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tms_repo_role',
            },
        ),
    ]
