from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


# Create your views here.
def get_index(request):
    return render(request, "index.html")


def news(request):
    return render(request, "news.html")


def login(request):
    if request.method == 'POST':
        data = request.data
        return JsonResponse(data)
    return render(request, "login.html")


# 在login图片的src是一个路由，根据这个路由找到urls.py里面对应的路由，从而找到views函数，这个函数直接访问生成的图片位置
# 最终给到前端
def get_random_code(request):
    fp = open(r'F:\PersonalBlogProject\app01\utils\new_img.png', 'rb')
    data = fp.read()
    fp.close()
    return HttpResponse(data)


def register(request):
    return render(request, "register.html")
