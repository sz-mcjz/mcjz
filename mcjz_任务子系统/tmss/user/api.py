import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render_to_response, reverse, redirect

from task.models import TaskLevel, Task, TaskModify, TaskCheck
from user.models import Staff, Department


def login(request, **kwargs):
    if request.method == 'GET':
        return render_to_response('login.html', context=kwargs)
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = Staff.objects.filter(telephone=username, password=password).first()
        if user:
            resp = redirect(reverse('index'))
            resp.set_cookie('uuid', user.telephone)
            return resp
        else:
            return render_to_response('login.html', context={'msg': '用户名或密码错误'})


def logout(request):
    if request.method == 'GET':
        res = redirect(reverse('login'))
        res.delete_cookie('uuid')
        return res


def index(request):
    if request.method == 'GET':
        uuid = request.COOKIES.get('uuid')
        user = Staff.objects.get(telephone=uuid)
        staff = [user for user in Staff.objects.all()]
        staff.remove(Staff.objects.get(telephone=uuid))
        # 我的任务
        completed_task = [complete_task.task_name_id for complete_task in
                          TaskCheck.objects.filter(task_recipient=user)]
        my_all_tasks = [task for task in Task.objects.filter(~Q(id__in=completed_task), task_recipient=user.username)]
        # 我的发布
        release_my_all_tasks = [task for task in Task.objects.filter(task_originator=user.username)]
        release_completed_task = [complete_task.task_name.id for complete_task in
                                  TaskCheck.objects.filter(task_name__in=release_my_all_tasks, is_complete=1)]
        release_my_all_tasks = [task for task in
                                Task.objects.filter(~Q(id__in=release_completed_task), task_originator=user.username)]
        # 今日到期
        now = datetime.datetime.now().date()  # 2020-01-02  查询今天到期的
        ids = TaskCheck.objects.filter(task_recipient=user,is_complete=1).values_list("task_name_id")# 已经提交的id集合
        all_task = Task.objects.filter(~Q(id__in=ids),task_end_time=now, task_recipient=user.username)
        # 逾期任务
        overtime_task = Task.objects.filter(~Q(id__in=ids),task_end_time__lt=now, task_recipient=user.username)
        overtime_tasks = []
        print("overtime_tasks--------------",overtime_tasks)
        for task in overtime_task:
            # 逾期时间为当前时间减去计划完成时间的天数
            task.yuqi_time = (now - task.task_end_time).days
            overtime_tasks.append(task)
        data = {
            'username': user.username,
            'icon': user.icon,
            'department': user.department.name,
            'telephone': user.telephone,
            'levels': [level for level in TaskLevel.objects.all()],
            'users': staff,
            'tasks': [task for task in all_task],
            'my_tasks':my_all_tasks,
            'releases': release_my_all_tasks,
            'overtime_tasks': overtime_tasks,
            'to_examines': [examine for examine in
                            TaskModify.objects.filter(task_name__task_originator=user.username, is_agree=0)],
            'submit_examines': [examine for examine in
                                TaskCheck.objects.filter(task_name__task_originator=user.username, is_complete=0)]
        }
        return render_to_response('index.html', context=data)
    if request.method == 'POST':
        uuid = request.COOKIES.get('uuid')
        user = Staff.objects.get(telephone=uuid)
        try:
            new_task = Task()
            new_task.task_originator = user.username
            new_task.task_recipient = request.POST.get('recipient')
            new_task.task_name = request.POST.get('content')
            new_task.task_level = TaskLevel.objects.get(name=request.POST.get('level'))
            new_task.task_start_time = request.POST.get('start_time')
            new_task.task_end_time = request.POST.get('end_time')
            new_task.mark = request.POST.get('mark')
            new_task.save()
            staff = [user for user in Staff.objects.all()]
            staff.remove(Staff.objects.get(telephone=uuid))
            data = {
                'username': user.username,
                'icon': user.icon,
                'department': user.department.name,
                'telephone': user.telephone,
                'levels': [level for level in TaskLevel.objects.all()],
                'users': staff,
                'tasks': [task for task in Task.objects.filter(task_recipient=user.username)],
                'releases': [task for task in Task.objects.filter(task_originator=user.username)],
            }
            return JsonResponse(data={'msg': '发布成功'}, json_dumps_params={'ensure_ascii': False})
        except:
            return JsonResponse(data={'msg': '发布失败'}, json_dumps_params={'ensure_ascii': False})


def profile(request):
    uuid = request.COOKIES.get('uuid')
    user = Staff.objects.get(telephone=uuid)
    if request.method == 'GET':
        phone = request.COOKIES.get('uuid', None)
        user = Staff.objects.get(telephone=phone)
        data = {
            'icon': user.icon,
            'username': user.username,
            'id_card': user.id_card,
            'telephone': phone,
            'password': user.password,
            'department': user.department.name,
        }
        return render_to_response('user/profile.html', context=data)
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        phone = request.COOKIES.get('uuid', None)
        user = Staff.objects.get(telephone=phone)
        if old_password and password and new_password:
            if user.password == old_password:
                if len(password) < 4:
                    return JsonResponse(data={"msg": "新密码不能小于4位。"}, json_dumps_params={'ensure_ascii': False})
                else:
                    if new_password == password:
                        obj = Staff.objects.get(telephone=user.telephone)
                        obj.password = password
                        obj.save()
                        return JsonResponse(data={'msg': '修改成功。'}, json_dumps_params={'ensure_ascii': False})
                    else:
                        return JsonResponse(data={'msg': '设置的两次新密码不一致。'}, json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse(data={"msg": "密码错误。"}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse(data={'msg': '内容不能为空。'}, json_dumps_params={'ensure_ascii': False})
