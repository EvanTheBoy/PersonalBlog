from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from app01.utils.generateCode import generate_random_code


# Create your views here.
def get_index(request):
    return render(request, "index.html")


def news(request):
    return render(request, "news.html")


def login(request):
    if request.method == 'POST':
        res = {
            'code': 1,  # 0表示登录成功
            'msg': "登录成功!",  # 提示信息
            'self': None  # 提示错误的地方
        }
        data = request.data
        name = data.get('name')
        if not name:
            res['msg'] = "请输入用户名!"
            res['self'] = "name"
            return JsonResponse(res)

        pwd = data.get('pwd')
        if not pwd:
            res['msg'] = "请输入密码!"
            res['self'] = "pwd"
            return JsonResponse(res)

        code = data.get('code')
        if not code:
            res['msg'] = "请输入验证码!"
            res['self'] = "code"
            return JsonResponse(res)

        # 校验验证码是否正确
        valid_code: str = request.session.get('valid_code')
        if valid_code.upper() != code.upper():
            res['msg'] = "验证码错误!"
            res["self"] = "code"
            return JsonResponse(res)

        # 校验用户名和密码有没有输对
        if name != "Evan" or pwd != "123456":
            res['msg'] = "用户名或密码错误!"
            res["self"] = "name"
            return JsonResponse(res)

        res['code'] = 0
        return JsonResponse(res)
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
