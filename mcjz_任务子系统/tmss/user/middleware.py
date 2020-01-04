from django.shortcuts import render, redirect, reverse
from django.utils.deprecation import MiddlewareMixin


class MyMiddleAware2(MiddlewareMixin):
    # 如果验证成功，则什么一个不用做，否则返回HttpResponse即可响应请求(中断)
    def process_request(self, request):  # 强制登录判断
        print(request.path)
        if "/login/" not in request.path:  # 路径中如果没有"login"
            # print("登录验证")
            # print(request)
            uuid = request.COOKIES.get('uuid', None)  # 获取session
            print(uuid)
            if uuid is None:  # 判断是否有登录的标记
                # print("未登录")
                return redirect(reverse('login'))  # 未登录则，跳转登录页面
            else:
                pass  # print('已登入')
        else:
            pass  # print("正在登录")  # 如果路径中"login"则是登录动作本身
