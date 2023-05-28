# Generated by Django 4.2.1 on 2023-05-28 10:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_repo_user_unique_un_role_constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repo_role',
            name='role_priority',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(99)]),
        ),
    ]