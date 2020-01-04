from django.http import HttpResponse
from django.shortcuts import render_to_response

from task.models import Task, TaskModify
import datetime

from django.shortcuts import render_to_response
from task.models import *
from task.models import Task, TaskCheck
from user.models import Staff

"""
所有任务：1.全部任务 2.已完成 3.未完成 4.当日任务 5.超时任务
"""


def all_task(request):
    uuid = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=uuid)
    tasks = Task.objects.all()
    now = datetime.datetime.now().date()
    tsk = []
    for task in tasks:
        time = task.taskcheck_set.all().values_list('timer')
        if time:
            for t in time:
                task.virtual_end_time = t[0]
                tsk.append(task)
        else:
            task.virtual_end_time = '未完成'
            tsk.append(task)

    tsk1 = []
    for t in tsk:
        if t.virtual_end_time == '未完成':
            days = now - t.task_end_time
            day = str(days)
            day = day.split('d')
            if day[0] == '0:00:00':
                day = 0
            else:
                day = int(day[0])

            if day > 0:
                t.yuqi = days.days
                tsk1.append(t)
            else:
                t.yuqi = 0
                tsk1.append(t)

        else:
            day = t.virtual_end_time - t.task_end_time
            t.yuqi = day.days
            tsk1.append(t)

    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'tasks': tsk1,
    }
    return render_to_response('task/all_task.html', context=data)


def finish_task(request):
    uuid = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=uuid)
    tasks = TaskCheck.objects.all()

    tsk = []
    for t in tasks:
        day = t.timer - t.task_name.task_end_time
        t.yuqi = day.days
        tsk.append(t)

    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'tasks': tsk,
    }
    return render_to_response('task/finish_task.html', context=data)


def incomplete_task(request):
    uuid = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=uuid)
    tasks = Task.objects.all()
    tasks1 = TaskCheck.objects.all()
    now = datetime.datetime.now().date()
    list_id = []
    for t in tasks:
        list_id.append(t.id)
    for t1 in tasks1:
        if t1.task_name_id in list_id:
            list_id.remove(t1.task_name_id)
    tasks2 = Task.objects.filter(id__in=list_id)

    tsk = []
    for task in tasks2:
        time = task.taskcheck_set.all().values_list('timer')
        if time:
            for t in time:
                task.virtual_end_time = t[0]
                tsk.append(task)
        else:
            task.virtual_end_time = '未完成'
            tsk.append(task)

    tsk1 = []
    for t in tsk:
        if t.virtual_end_time == '未完成':
            days = now - t.task_end_time
            day = str(days)
            day = day.split('d')
            if day[0] == '0:00:00':
                day = 0
            else:
                day = int(day[0])

            if day > 0:
                t.yuqi = days.days
                tsk1.append(t)
            else:
                t.yuqi = 0
                tsk1.append(t)

        else:
            day = t.virtual_end_time - t.task_end_time
            t.yuqi = day.days
            tsk1.append(t)

    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'tasks': tsk1,
    }
    return render_to_response('task/incomplete_task.html', context=data)


def current_task(request):
    uuid = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=uuid)
    now = datetime.datetime.now().date()
    tasks = Task.objects.filter(task_end_time=now)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'tasks': tasks,
    }
    return render_to_response('task/current_task.html', context=data)


def overtime_task(request):
    uuid = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=uuid)
    now = datetime.datetime.now().date()
    tasks = Task.objects.all()
    tsk = []
    for task in tasks:
        time = task.taskcheck_set.all().values_list('timer')
        if time:
            for t in time:
                task.virtual_end_time = t[0]
                tsk.append(task)
        else:
            task.virtual_end_time = '未完成'
            tsk.append(task)

    tsk1 = []
    for t in tsk:
        if t.virtual_end_time == '未完成':
            days = now - t.task_end_time
            day = str(days)
            day = day.split('d')
            if day[0] == '0:00:00':
                day = 0
            else:
                day = int(day[0])

            if day > 0:
                t.yuqi = days.days
                tsk1.append(t)
            else:
                t.yuqi = 0
                tsk1.append(t)

        else:
            day = t.virtual_end_time - t.task_end_time
            t.yuqi = day.days
            tsk1.append(t)

        for i in tsk1:
            if i.yuqi == 0:
                tsk1.remove(i)

    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'tasks': tsk1,
    }
    return render_to_response('task/overtime_task.html', context=data)


"""
我的任务：1.全部任务 2.已完成 3.未完成 4.当日任务 5.超时任务
"""


def my_all_task(request):
    uuid = request.COOKIES.get('uuid')
    print(uuid)
    user = Staff.objects.get(telephone=uuid)
    all_task = Task.objects.filter(task_recipient=user.username)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': [task for task in all_task],
    }
    return render_to_response('my_receive/my_all_task.html', context=data)

# 我的任务 已完成
def my_finish_task(request):
    uuid = request.COOKIES.get('uuid')
    print(uuid)
    user = Staff.objects.get(telephone=uuid)
    all_task = TaskCheck.objects.filter(task_recipient=user, is_complete=1).values_list("task_name")
    tasks = Task.objects.filter(id__in=all_task)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': tasks,
    }
    return render_to_response('my_receive/my_finish_task.html', context=data)

from django.db.models import Q
# 我的任务 未完成
def my_incomplete_task(request):
    uuid = request.COOKIES.get('uuid')
    print(uuid)
    user = Staff.objects.get(telephone=uuid)
    # 责任人为我 查询TaskCheck中不存在的对象
    all_task = TaskCheck.objects.filter(task_recipient=user).values_list("task_name_id")
    tasks = Task.objects.filter(~Q(id__in=all_task),task_recipient=user.username)

    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': tasks,
    }
    return render_to_response('my_receive/my_incomplete_task.html', context=data)

# 我的任务 当天到期
def my_current_task(request):
    uuid = request.COOKIES.get('uuid')
    print(uuid)
    user = Staff.objects.get(telephone=uuid)
    now = datetime.datetime.now().date()  # 2020-01-02  查询今天到期的
    all_task = Task.objects.filter(task_end_time=now, task_recipient=user.username)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': [task for task in all_task],
    }
    return render_to_response('my_receive/my_current_task.html', context=data)

# 我的任务  超时的
def my_overtime_task(request):
    uuid = request.COOKIES.get('uuid')
    print(uuid)
    user = Staff.objects.get(telephone=uuid)
    now = datetime.datetime.now().date()  # 2020-01-02  如果时间小于当前时间则逾期
    all_task = Task.objects.filter(task_end_time__lt=now, task_recipient=user.username)
    tasks = []
    for task in all_task:
        # 逾期时间为当前时间减去计划完成时间的天数
        task.yuqi_time = (now - task.task_end_time).days
        tasks.append(task)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': tasks,
    }
    return render_to_response('my_receive/my_overtime_task.html', context=data)


"""
我的发布：1.全部任务 2.已完成 3.未完成 4.当日任务 5.超时任务
"""


#  查询所有的
def my_release_all_task(request):
    uuid = request.COOKIES.get('uuid')
    # print(uuid)
    user = Staff.objects.get(telephone=uuid)
    all_task = Task.objects.filter(task_originator=user.username)
    print(all_task)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': [task for task in all_task],
    }

    return render_to_response('my_release/my_release_all_task.html', context=data)


# 查询已完成的
def my_release_finish_task(request):
    uuid = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=uuid)
    print(user.username)
    all_task = TaskCheck.objects.filter(task_name__task_originator=user.username, is_complete=1).values_list(
        "task_name_id")
    print()
    tasks = Task.objects.filter(id__in=all_task)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': tasks,
    }
    return render_to_response('my_release/my_release_finish_task.html', context=data)


# 查询未完成的
def my_release_incomplete_task(request):
    uuid = request.COOKIES.get('uuid')
    print(uuid)
    user = Staff.objects.get(telephone=uuid)
    # 未完成的任务  把已完成的过滤掉
    # 先获取已完成的 任务id   条件为
    ftask = TaskCheck.objects.filter(task_name__task_originator=user.username, is_complete=1).values_list("task_name_id")
    # 过滤掉已完成的任务id  条件为反向上述条件，同时是自己
    tasks = Task.objects.filter(~Q(id__in=ftask),task_originator=user.username)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': tasks,
    }
    return render_to_response('my_release/my_release_incomplete_task.html', context=data)


import datetime


# 查询当天到期的
def my_release_current_task(request):
    uuid = request.COOKIES.get('uuid')
    print(uuid)
    user = Staff.objects.get(telephone=uuid)
    now = datetime.datetime.now().date()  # 2020-01-02  查询今天到期的
    all_task = Task.objects.filter(task_end_time=now, task_originator=user.username)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': [task for task in all_task],
    }
    return render_to_response('my_release/my_release_current_task.html', context=data)


# 查询超时任务
def my_release_overtime_task(request):
    uuid = request.COOKIES.get('uuid')
    print(uuid)
    user = Staff.objects.get(telephone=uuid)
    now = datetime.datetime.now().date()  # 2020-01-02  如果时间小于当前时间则逾期   逾期为：未完成+截止时间小于今天
    # all_task = TaskCheck.objects.filter(task_name__task_originator=user.username, is_complete=0).values_list("task_name_id")
    all_task = Task.objects.filter(task_end_time__lt=now, task_originator=user.username)
    tasks = []
    for task in all_task:
        # 逾期时间为当前时间减去计划完成时间的天数
        task.yuqi_time = (now - task.task_end_time).days
        tasks.append(task)

    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': tasks,
    }
    return render_to_response('my_release/my_release_overtime_task.html', context=data)


# 删除任务
def task_delete(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        Task.objects.filter(id=task_id).delete()
        return render_to_response('index.html')


# 修改任务
def task_modify(request):
    telephone = request.COOKIES.get('uuid', None)
    if request.method == 'POST':
        task_id = request.POST.get('task_id', None)
        task_modify_end_time = request.POST.get('modify_end_time', None)
        # 向TaskModify表生成修改记录
        # 修改task表时间
        temp = Task.objects.get(id=task_id)
        if Staff.objects.get(telephone=telephone).username == temp.task_originator:
            modify = TaskModify()
            modify.task_name = temp
            modify.task_modify_applicant = temp.task_recipient
            modify.task_origin_end_time = temp.task_end_time
            modify.task_modify_end_time = task_modify_end_time
            modify.is_agree = True
            modify.save()
            # 修改task表
            temp.task_end_time = task_modify_end_time
            temp.save()
            return HttpResponse('ok')
        else:
            modify = TaskModify()
            modify.task_name = temp
            modify.task_modify_applicant = temp.task_recipient
            modify.task_origin_end_time = temp.task_end_time
            modify.task_modify_end_time = task_modify_end_time
            modify.save()
            return HttpResponse('ok')
    else:
        return HttpResponse('failed')


# 延期任务申请
def task_delay(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task_modify_end_time = request.POST.get('modify_end_time')
        temp = Task.objects.get(id=task_id)
        # 向TaskModify表生成修改数据
        modify = TaskModify()
        modify.task_name = temp
        modify.task_modify_applicant = temp.task_recipient
        modify.task_origin_end_time = temp.task_end_time
        modify.task_modify_end_time = task_modify_end_time
        modify.save()
        return HttpResponse('ok')


# 任务延期审核
def task_to_examine(request):
    modify_id = request.POST.get("modify_id")
    change = TaskModify.objects.get(id=modify_id)
    change.is_agree = 1
    change.save()
    origin_task = Task.objects.get(id=change.task_name_id)
    origin_task.task_end_time = change.task_modify_end_time
    origin_task.save()
    return HttpResponse('ok')


# 任务提交
def task_to_submit(request):
    task_id = request.POST.get('task_id')
    submit_task = TaskCheck()
    submit_task.task_name = Task.objects.get(id=task_id)
    submit_task.task_recipient = Staff.objects.get(username=Task.objects.get(id=task_id).task_recipient)
    submit_task.save()
    return HttpResponse("ok")


# 任务通过审核
def examine_submit_task(request):
    task_id = request.POST.get('task_id')
    examine_task = TaskCheck.objects.get(id=task_id)
    examine_task.is_complete = 1
    examine_task.save()
    return HttpResponse('ok')

"""
统计分析
"""


def analysis(request):
    telephone = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=telephone)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
    }
    return render_to_response('analysis.html', context=data)
