# 这个app的views只返回页面，所有的ajax请求全部放到新创建的那个api的login里去。
# 其目的就是把跟请求相关的代码从这个视图中分离出去

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.utils.generateCode import generate_random_code

from django.contrib import auth
from app01.models import UserInfo


# Create your views here.


def get_index(request):
    return render(request, "index.html", {"request": request})


def news(request):
    return render(request, "news.html")


def login(request):
    return render(request, "login.html")


# 在login图片的src是一个路由，根据这个路由找到urls.py里面对应的路由，从而找到views函数，这个函数直接访问生成的图片位置
# 最终给到前端
# 前端确实可以拿到code，但是后端怎么知道正不正确呢？把验证码放到每个人都有的那个地方就可以了，就是session
def get_random_code(request):
    data, valid_code = generate_random_code()
    # 将验证码写入session
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


def register(request):
    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect('/')
