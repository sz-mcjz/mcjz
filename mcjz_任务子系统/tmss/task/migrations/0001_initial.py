# Generated by Django 2.2 on 2020-01-02 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_originator', models.CharField(max_length=125)),
                ('task_recipient', models.CharField(max_length=125)),
                ('task_name', models.CharField(max_length=125)),
                ('release_time', models.DateTimeField(auto_now_add=True)),
                ('task_start_time', models.DateField()),
                ('task_end_time', models.DateField()),
                ('mark', models.TextField()),
            ],
            options={
                'db_table': 'mcjz_task',
            },
        ),
        migrations.CreateModel(
            name='TaskLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
            ],
            options={
                'db_table': 'mcjz_task_level',
            },
        ),
        migrations.CreateModel(
            name='TaskModify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_modify_applicant', models.CharField(max_length=125)),
                ('task_modify_time', models.DateTimeField(auto_now_add=True)),
                ('task_origin_end_time', models.DateField()),
                ('task_modify_end_time', models.DateField()),
                ('task_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Task')),
            ],
            options={
                'db_table': 'mcjz_task_modify',
            },
        ),
        migrations.CreateModel(
            name='TaskCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_complete', models.BooleanField(default=False)),
                ('timer', models.DateField(auto_now_add=True)),
                ('task_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Task')),
                ('task_recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Staff')),
            ],
            options={
                'db_table': 'mcjz_task_check',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='task_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.TaskLevel'),
        ),
    ]
