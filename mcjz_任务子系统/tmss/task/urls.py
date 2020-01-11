from django.urls import path

from task import api

urlpatterns = [
    # 所有任务
    path('all/task/', api.all_task, name='all_task'),
    path('finish/task', api.finish_task, name='finish_task'),
    path('incomplete/task', api.incomplete_task, name='incomplete_task'),
    path('current/task', api.current_task, name='current_task'),
    path('overtime/task', api.overtime_task, name='overtime_task'),
    path('advance/task', api.advance_task, name='advance_task'),
    # 我的任务
    path('my/all/task/', api.my_all_task, name='my_all_task'),
    path('my/finish/task', api.my_finish_task, name='my_finish_task'),
    path('my/incomplete/task', api.my_incomplete_task, name='my_incomplete_task'),
    path('my/current/task', api.my_current_task, name='my_current_task'),
    path('my/overtime/task', api.my_overtime_task, name='my_overtime_task'),
    # 我的发布
    path('release/all/task/', api.my_release_all_task, name='my_release_all_task'),
    path('release/finish/task', api.my_release_finish_task, name='my_release_finish_task'),
    path('release/incomplete/task', api.my_release_incomplete_task, name='my_release_incomplete_task'),
    path('release/current/task', api.my_release_current_task, name='my_release_current_task'),
    path('release/overtime/task', api.my_release_overtime_task, name='my_release_overtime_task'),

    # 删除
    path('my/release/task/delete/', api.task_delete, name='delete_my_task'),
    # 修改
    path('my/release/task/modify/', api.task_modify, name='modify_my_task'),
    # 延期申请
    path('my/release/task/delay/', api.task_delay, name='delay_my_task'),
    # 延期审核
    path('my/release/task/examine/', api.task_to_examine, name='examine_task'),
    # 任务提交
    path('my/receive/task/submit/', api.task_to_submit, name='submit_task'),
    # 任务通过审核
    path('my/examine/submit/task/', api.examine_submit_task, name='examine_submit_task'),
    # 个人统计
    path('analysis/', api.analysis, name='analysis'),
    # 综合统计
    path('analysis2/', api.analysis2, name='analysis2'),
    # 按天统计
    path('analysis3/', api.analysis3, name='analysis3'),
    # 组织架构
    path('structure/', api.structure, name='structure'),
]
