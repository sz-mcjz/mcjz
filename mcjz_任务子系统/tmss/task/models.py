from django.db import models

from user.models import Staff


class TaskLevel(models.Model):
    name = models.CharField(max_length=125)

    class Meta:
        db_table = 'mcjz_task_level'


class Task(models.Model):
    task_originator = models.CharField(max_length=125)  # 任务发起人
    task_recipient = models.CharField(max_length=125)  # 待办责任人
    task_name = models.CharField(max_length=125)  # 任务内容
    task_level = models.ForeignKey('TaskLevel', on_delete=models.CASCADE)  # 任务等级
    release_time = models.DateTimeField(auto_now_add=True)  # 发布时间
    task_start_time = models.DateField()  # 任务开始时间
    task_end_time = models.DateField()  # 计划完成时间
    mark = models.TextField()

    class Meta:
        db_table = 'mcjz_task'


class TaskModify(models.Model):
    task_name = models.ForeignKey('Task', on_delete=models.CASCADE)  # 任务内容
    task_modify_applicant = models.CharField(max_length=125)  # 任务修改申请人
    task_modify_time = models.DateTimeField(auto_now_add=True)  # 修改时间
    task_origin_end_time = models.DateField()  # 任务原来的结束时间
    task_modify_end_time = models.DateField()  # 任务修改后的结束时间
    is_agree = models.BooleanField(default=False)  # 任务修改后是否同意

    class Meta:
        db_table = 'mcjz_task_modify'


class TaskCheck(models.Model):
    task_name = models.ForeignKey('Task', on_delete=models.CASCADE)  # 任务内容
    task_recipient = models.ForeignKey(Staff, related_name='recipient', on_delete=models.CASCADE)  # 任务代办责任人
    is_complete = models.BooleanField(default=False)  # 是否完成
    timer = models.DateField(auto_now_add=True)  # 完成时间

    class Meta:
        db_table = 'mcjz_task_check'
