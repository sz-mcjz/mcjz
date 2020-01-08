from django.db import connection
from django.http import HttpResponse, JsonResponse
import datetime

from django.shortcuts import render_to_response
from task.models import *
from task.models import Task, TaskCheck
from user.models import Staff
from django.db.models import Q

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
    tasks = TaskCheck.objects.filter(is_complete=1)

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
    tasks1 = TaskCheck.objects.filter(is_complete=1)
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


def advance_task(request):
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
    return render_to_response('task/advance_task.html', context=data)


"""
我的任务：1.全部任务 2.已完成 3.未完成 4.当日任务 5.超时任务
"""


def my_all_task(request):
    uuid = request.COOKIES.get('uuid')
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


# 我的任务 未完成
def my_incomplete_task(request):
    uuid = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=uuid)
    # 责任人为我 查询TaskCheck中不存在的对象
    all_task = TaskCheck.objects.filter(task_recipient=user, is_complete=1).values_list("task_name_id")
    tasks = Task.objects.filter(~Q(id__in=all_task), task_recipient=user.username)

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
    user = Staff.objects.get(telephone=uuid)
    all_task = Task.objects.filter(task_originator=user.username)
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
    all_task = TaskCheck.objects.filter(task_name__task_originator=user.username, is_complete=1).values_list(
        "task_name_id")
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
    user = Staff.objects.get(telephone=uuid)
    # 未完成的任务  把已完成的过滤掉
    # 先获取已完成的 任务id   条件为
    ftask = TaskCheck.objects.filter(task_name__task_originator=user.username, is_complete=1).values_list(
        "task_name_id")
    # 过滤掉已完成的任务id  条件为反向上述条件，同时是自己
    tasks = Task.objects.filter(~Q(id__in=ftask), task_originator=user.username)
    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'all_task': tasks,
    }
    return render_to_response('my_release/my_release_incomplete_task.html', context=data)


# 查询当天到期的
def my_release_current_task(request):
    uuid = request.COOKIES.get('uuid')
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
    user = Staff.objects.get(telephone=telephone)
    if request.method == 'POST':
        task_id = request.POST.get('task_id', None)
        task_modify_end_time = request.POST.get('modify_end_time', None)
        # 向TaskModify表生成修改记录
        # 修改task表时间
        temp = Task.objects.get(id=task_id)
        if user.username == temp.task_originator:
            modify = TaskModify()
            modify.task_name = temp
            modify.task_modify_applicant = temp.task_recipient
            modify.task_origin_end_time = temp.task_end_time
            modify.task_modify_end_time = task_modify_end_time
            modify.is_agree = 1
            modify.save()
            # 修改task表
            temp.task_end_time = task_modify_end_time
            temp.save()
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


# 统计分析
def analysis(request):
    telephone = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=telephone)
    users = Staff.objects.all()

    cursor = connection.cursor()
    cursor.execute('SELECT task_originator,COUNT(*) FROM mcjz_task GROUP BY task_originator')  # 所有我发布的

    row = cursor.fetchall()
    cursor.execute('SELECT task_recipient,COUNT(*) FROM mcjz_task GROUP BY task_recipient')  # 所有我要做的

    row1 = cursor.fetchall()
    cursor.execute(
        'SELECT task_originator,COUNT(*) FROM mcjz_task a inner join mcjz_task_check b on a.id = b.task_name_id  WHERE is_complete=1 GROUP BY task_originator ')  # 所有我发布已经完成的
    row2 = cursor.fetchall()

    cursor.execute(
        'SELECT task_recipient,COUNT(*) FROM mcjz_task a inner join mcjz_task_check b on a.id = b.task_name_id  WHERE is_complete=1 GROUP BY task_recipient ')  # 所有我办的已经完成的
    row3 = cursor.fetchall()

    cursor.execute(
        "select task_originator,count(task_originator) from mcjz_task where mcjz_task.id not in (select task_name_id from mcjz_task_check where is_complete = '1') group by task_originator")
    row4 = cursor.fetchall()

    cursor.execute(
        "select task_recipient,count(task_recipient) from mcjz_task where mcjz_task.id not in (select task_name_id from mcjz_task_check where is_complete = '1') group by task_recipient")
    row5 = cursor.fetchall()

    cursor.execute(
        'SELECT task_originator,COUNT(*) FROM mcjz_task  WHERE task_end_time=(select curdate()) GROUP BY task_originator')  # 我发布的今天预期
    row6 = cursor.fetchall()

    cursor.execute(
        'SELECT task_recipient,COUNT(*) FROM mcjz_task  WHERE task_end_time=(select curdate()) GROUP BY task_recipient')  # 我要做的今天预期
    row7 = cursor.fetchall()

    cursor.execute(
        "select task_originator,count(task_originator) from mcjz_task where task_end_time < DATE_FORMAT(now(),'%Y-%m-%d') and id not in (select task_name_id from mcjz_task_check,mcjz_task where task_name_id = mcjz_task.id and mcjz_task_check.is_complete = '1' and mcjz_task_check.timer <= mcjz_task.task_end_time) group by task_originator")
    # 我发布的今天预期
    row8 = cursor.fetchall()

    cursor.execute(
        "select task_recipient,count(task_recipient) from mcjz_task where task_end_time < DATE_FORMAT(now(),'%Y-%m-%d') and id not in (select task_name_id from mcjz_task_check,mcjz_task where task_name_id = mcjz_task.id and mcjz_task_check.is_complete = '1' and mcjz_task_check.timer <= mcjz_task.task_end_time) group by task_recipient")
    row9 = cursor.fetchall()

    max_number = 0
    user_list = []
    for user in users:
        user_list.append(user.username)

    row_list = [row, row2, row4, row6, row8]
    all_list = []

    for u in user_list:
        name_list = []
        i = 1
        for row in row_list:
            for r in row:
                if u == r[0]:
                    name_list.append(r[1])
                    if r[1] > max_number:
                        max_number = r[1]
            if len(name_list) != i:
                name_list.append(0)
            i += 1
        all_list.append(name_list)

    row_list = [row1, row3, row5, row7, row9]
    all_list2 = []
    max_number2 = max_number
    for u in user_list:
        name_list = []
        i = 1
        for row in row_list:
            for r in row:
                if u == r[0]:
                    name_list.append(r[1])
                    if r[1] > max_number2:
                        max_number2 = r[1]

            if len(name_list) != i:
                name_list.append(0)
            i += 1
        all_list2.append(name_list)

    print(max_number2)
    user1 = []
    i = 0
    for user in users:
        user.numb = all_list[i]
        user.numb1 = all_list2[i]
        user1.append(user)
        i += 1

    data = {
        'username': user.username,
        'icon': user.icon,
        'department': user.department.name,
        'users': user1,
        'max': max_number2,
    }
    return render_to_response('analysis.html', context=data)


def sort(ret, user, sortby):
    # 把 总经理 和 副经理 单独掉出来排1和2，自身排3
    lis = list(ret)  # [('石龙进', 4), ('阳瑞', 16), ('陈林', 1)]
    usernames = list(Staff.objects.all().values("username"))
    count = []
    for i in lis:
        if ((list(i))[0]) == user.username:
            count.append(list(i))
            lis.remove(i)
        elif ((list(i))[0]) == "总经理":
            count.append(list(i))
            lis.remove(i)
        elif ((list(i))[0]) == "副总":
            count.append(list(i))
            lis.remove(i)
    lis2 = [list(i) for i in lis]
    count = count + lis2  # 两个列表相连
    temp = list(zip(*count[::-1]))
    result = [list(t) for t in temp]  # [['陈林', '阳瑞', '石龙进'], [1, 16, 4]]
    # 为  0  用户的追加
    for username in usernames:
        if username["username"] not in result[0]:
            result[0].insert(0, username["username"])
            result[1].insert(0, 0)

    if sortby != None and sortby != "":  # 用于排序的代码
        dic = []
        for num in range(len(result[0])):
            dic.append({"name": result[0][num], "value": result[1][num]})
        new_dic = []
        if sortby == "count":
            new_dic = sorted(dic, key=lambda x: x["value"])  # 按照数量排序  在此处倒序在前端就是正序
        elif sortby == "name":
            dic = [{"name": i["name"].encode("GBK"), "value": i["value"]} for i in dic]
            new_dic = sorted(dic, reverse=True, key=lambda x: x["name"])  # 按照名字排序  在此处倒序在前端就是正序
            new_dic = [{"name": i["name"].decode("GBK"), "value": i["value"]} for i in new_dic]

        new_list = [[], []]
        for d in new_dic:
            new_list[0].append(d["name"])
            new_list[1].append(d["value"])
        result = new_list
    return result


def analysis2(request):
    telephone = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=telephone)
    # 所有员工
    staffs = Staff.objects.all()
    # 查询已发布 按用户名分组 统计个数，
    if request.method == "GET":
        data = {
            'username': user.username,
            'icon': user.icon,
            'department': user.department.name,
        }
        return render_to_response('analysis2.html', context=data)

    elif request.method == 'POST':
        sortby = request.POST.get("sortby")
        cursor = connection.cursor()
        cursor.execute(
            'select task_originator,COUNT(task_originator) task_count from mcjz_task GROUP BY task_originator')
        ret = None
        try:
            ret = cursor.fetchall()
        except:
            return JsonResponse({"code": 500, "msg": "error", "data": {"data": None}})
        release_count = sort(ret, user, sortby)  # 参数为查询集和当前用户
        # print("已发布任务统计",release_count )

        # 已完成
        # 查询 已完成的统计
        cursor.execute(
            "select username,count(task_recipient_id) from mcjz_staff,mcjz_task_check where mcjz_staff.id = mcjz_task_check.task_recipient_id and mcjz_task_check.is_complete='1' GROUP BY task_recipient_id")
        try:
            ret = cursor.fetchall()
        except:
            return JsonResponse({"code": 500, "msg": "error", "data": {"data": None}})
        finish_count = sort(ret, user, sortby)
        # print("已完成任务统计", finish_count)

        # 待办
        cursor.execute(
            "select task_recipient,count(task_recipient) from mcjz_task where mcjz_task.id not in (select task_name_id from mcjz_task_check where is_complete = '1') group by task_recipient")
        try:
            ret = cursor.fetchall()
        except:
            return JsonResponse({"code": 500, "msg": "error", "data": {"data": None}})
        wait_count = sort(ret, user, sortby)
        # print("待办任务统计", wait_count)

        # 发布逾期 你发布的，别人逾期的   数据库now()只取年月日：DATE_FORMAT(now(),'%Y-%m-%d')
        # select task_name_id from mcjz_task_check,mcjz_task where task_name_id = mcjz_task.id and mcjz_task_check.is_complete = '1' and mcjz_task_check.timer <= mcjz_task.task_end_time
        cursor.execute(
            "select task_originator,count(task_originator) from mcjz_task where task_end_time < DATE_FORMAT(now(),'%Y-%m-%d') and id not in (select task_name_id from mcjz_task_check,mcjz_task where task_name_id = mcjz_task.id and mcjz_task_check.is_complete = '1' and mcjz_task_check.timer <= mcjz_task.task_end_time) group by task_originator")
        try:
            ret = cursor.fetchall()
        except:
            return JsonResponse({"code": 500, "msg": "error", "data": {"data": None}})
        release_overdue_count = sort(ret, user, sortby)
        # print("发布逾期任务统计", release_overdue_count)

        # 待办逾期 别人发给我的任务，我逾期的
        cursor.execute(
            "select task_recipient,count(task_recipient) from mcjz_task where task_end_time < DATE_FORMAT(now(),'%Y-%m-%d') and id not in (select task_name_id from mcjz_task_check,mcjz_task where task_name_id = mcjz_task.id and mcjz_task_check.is_complete = '1' and mcjz_task_check.timer <= mcjz_task.task_end_time) group by task_recipient")
        try:
            ret = cursor.fetchall()
        except:
            return JsonResponse({"code": 500, "msg": "error", "data": {"data": None}})
        f_overdue_count = sort(ret, user, sortby)
        # print("待办逾期任务统计", f_overdue_count)

        # 逾期   所有人逾期任务天数
        cursor.execute(
            "select task_recipient,sum(datediff(now(),task_end_time)) num from mcjz_task where task_end_time < DATE_FORMAT(now(),'%Y-%m-%d') and id not in (select task_name_id from mcjz_task_check,mcjz_task where task_name_id = mcjz_task.id and mcjz_task_check.is_complete = '1' and mcjz_task_check.timer <= mcjz_task.task_end_time) group by task_recipient")
        try:
            ret = cursor.fetchall()
        except:
            return JsonResponse({"code": 500, "msg": "error", "data": {"data": None}})
        day_overdue_count = sort(ret, user, sortby)
        day_overdue_count[1] = [int(i) for i in day_overdue_count[1]]
        # print("逾期总天数统计", day_overdue_count)
        cursor.close()  # 查询完成后关闭游标
        lis = ['已发布(' + str(sum(release_count[1])) + ")", '已完成(' + str(sum(finish_count[1])) + ")",
               '待办(' + str(sum(wait_count[1])) + ")", '发布逾期(' + str(sum(release_overdue_count[1])) + ")",
               '待办逾期(' + str(sum(f_overdue_count[1])) + ")", '总逾期天数(' + str(sum(day_overdue_count[1])) + ")"]
        # 数据列表
        data_list = []
        data_list.append(release_count)
        data_list.append(finish_count)
        data_list.append(wait_count)
        data_list.append(release_overdue_count)
        data_list.append(f_overdue_count)
        data_list.append(day_overdue_count)

        return JsonResponse({"code": 200, "msg": "success", "data": {"data": data_list, "lis": lis}})


def analysis3(request):
    telephone = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=telephone)
    # 查询已发布 按用户名分组 统计个数，
    cursor = connection.cursor()
    if request.method == "GET":
        # 默认为 查询今天的
        data = {
            'username': user.username,
            'icon': user.icon,
            'department': user.department.name,
        }
        return render_to_response('analysis3.html', context=data)

    elif request.method == 'POST':
        sortby = request.POST.get("sortby")
        daynum = request.POST.get("daynum")
        if not daynum or daynum == "":
            daynum = "0"
        #       0 是今天 1两天内 2三天内 3四天内 4五天内 5六天内 6七天内
        # -- 查询所有人 n 天内发布的
        # -- select task_originator,count(task_originator) from mcjz_task where DATE_FORMAT(release_time,'%Y-%m-%d') between DATE_FORMAT(DATE_SUB(now(), INTERVAL 6 DAY),'%Y-%m-%d') and DATE_FORMAT(now(),'%Y-%m-%d') group by task_originator
        cursor.execute(
            "select task_originator,count(task_originator) from mcjz_task where DATE_FORMAT(release_time,'%Y-%m-%d') between DATE_FORMAT(DATE_SUB(now(), INTERVAL " + daynum + " DAY),'%Y-%m-%d') and DATE_FORMAT(now(),'%Y-%m-%d') group by task_originator")
        ret = None
        sen_count = None
        try:
            ret = cursor.fetchall()
            sen_count = sort(ret, user, sortby)  # 参数为查询集和当前用户
        except:
            return JsonResponse({"code": 500, "msg": "error", "data": {"data": "未查到信息"}})

        # -- 查询所有人 n 天内完成的
        # -- select task_recipient,count(task_recipient) from mcjz_task,mcjz_task_check where  mcjz_task.id=mcjz_task_check.task_name_id and is_complete='1' and DATE_FORMAT(mcjz_task_check.timer,'%Y-%m-%d') between DATE_FORMAT(DATE_SUB(now(), INTERVAL 6 DAY),'%Y-%m-%d') and DATE_FORMAT(now(),'%Y-%m-%d') group by task_recipient
        cursor.execute(
            "select task_recipient,count(task_recipient) from mcjz_task,mcjz_task_check where  mcjz_task.id=mcjz_task_check.task_name_id and is_complete='1' and DATE_FORMAT(mcjz_task_check.timer,'%Y-%m-%d') between DATE_FORMAT(DATE_SUB(now(), INTERVAL " + daynum + " DAY),'%Y-%m-%d') and DATE_FORMAT(now(),'%Y-%m-%d') group by task_recipient")
        fin_count = None
        try:
            ret = cursor.fetchall()
            fin_count = sort(ret, user, sortby)  # 参数为查询集和当前用户
        except:
            return JsonResponse({"code": 500, "msg": "error", "data": {"data": "未查到信息"}})
        data_list = []
        data_list.append(sen_count)
        data_list.append(fin_count)
        return JsonResponse(
            {"code": 200, "msg": "success",
             "data": {"data": data_list,
                      "lis": ["已发布统计(" + str(sum(sen_count[1])) + ")", "已完成统计(" + str(sum(fin_count[1])) + ")"], "sortby": sortby,
                      "daynum": daynum}})
