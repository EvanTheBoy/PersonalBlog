# 这个app的views只返回页面，所有的ajax请求全部放到新创建的那个api的login里去。
# 其目的就是把跟请求相关的代码从这个视图中分离出去

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.utils.generateCode import generate_random_code

from django.contrib import auth
from app01.models import UserInfo
from app01.models import Articles, Tags, Cover


# Create your views here.


def get_index(request):
    # 以下render函数的第三个参数，就保证了request可以在前端页面中被用到
    return render(request, "index.html", {"request": request})


def news(request):
    return render(request, "news.html")


def login(request):
    return render(request, "login.html")


# 在login图片的src是一个路由，根据这个路由找到urls.py里面对应的路由，从而找到views函数，这个函数直接访问生成的图片位置
# 最终给到前端
# 前端确实可以拿到code，但是后端怎么知道正不正确呢？把验证码放到每个人都有的那个地方就可以了，就是session
def get_random_code(request):
    # 调用下面这个函数，就得到了验证码存储在计算机中的信息和人眼中的信息
    data, valid_code = generate_random_code()
    # 将验证码写入session，这是为了保证每个人拿到的都不一样
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


def register(request):
    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


# 该方法返回文章详情页面，nid即文章的id号，表示该文章是第几篇文章
def article(request, nid):
    # 根据下面这个方法，依靠文章的id查询具体的文章
    article_query = Articles.objects.filter(nid=nid)
    if not article_query:
        # 若找不到，直接重定向回首页
        return redirect("/")
    passage = article_query.first()
    return render(request, 'article.html', locals())  # locals()方法表示把所有的东西都传给前端，不需要单独写{"nid": nid}了


# 后台个人中心
def backend(request):
    if not request.user.username:
        return redirect("/")
    return render(request, 'backend/backend.html', locals())


# 添加文章
def add_article(request):
    tag_list = Tags.objects.all()
    cover_list = Cover.objects.all()
    return render(request, 'backend/add_article.html', locals())


# 修改头像
def edit_avatar(request):
    return render(request, 'backend/edit_avatar.html', locals())


# 重置密码
def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())
