# Generated by Django 5.2.1 on 2025-06-03 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_first_name_user_last_name_user_middle_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='title',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('learner', 'Learner'), ('instructor', 'Instructor'), ('admin', 'Admin')], default='learner', max_length=20, verbose_name='Role/Title'),
        ),
    ]
