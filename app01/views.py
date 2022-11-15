from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from app01.utils.generateCode import generate_random_code
from django import forms


# Create your views here.

class LoginForm(forms.Form):
    name = forms.CharField(error_messages={"required": "请输入用户名"})
    pwd = forms.CharField(error_messages={"required": "请输入密码"})
    code = forms.CharField(error_messages={"required": "请输入验证码"})

    # 定义全局钩子
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        # 为字段添加错误信息
        if name != "evan" or pwd != "12345":
            self.add_error("pwd", "用户名或密码错误!")
        return self.cleaned_data


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

        form = LoginForm(data)
        if not form.is_valid():
            # 验证不通过
            # 将错误信息存在一个字典中
            err_dict: dict = form.errors
            # 拿到所有错误字段的名字，比如name, pwd这些。通过取得字典的key值可以拿到它们
            err_valid = list(err_dict.keys())[0]
            # 拿到第一个字段的错误信息,比如“请输入用户名”这样的信息
            err_msg = err_dict[err_valid][0]
            # 配置res的三个信息
            res['msg'] = err_msg
            res['self'] = err_valid
            return JsonResponse(res)

        # name = data.get('name')
        # if not name:
        #     res['msg'] = "请输入用户名!"
        #     res['self'] = "name"
        #     return JsonResponse(res)
        #
        # pwd = data.get('pwd')
        # if not pwd:
        #     res['msg'] = "请输入密码!"
        #     res['self'] = "pwd"
        #     return JsonResponse(res)
        #
        # code = data.get('code')
        # if not code:
        #     res['msg'] = "请输入验证码!"
        #     res['self'] = "code"
        #     return JsonResponse(res)
        #
        # # 校验验证码是否正确
        # valid_code: str = request.session.get('valid_code')
        # if valid_code.upper() != code.upper():
        #     res['msg'] = "验证码错误!"
        #     res["self"] = "code"
        #     return JsonResponse(res)
        #
        # # 校验用户名和密码有没有输对
        # if name != "Evan" or pwd != "123456":
        #     res['msg'] = "用户名或密码错误!"
        #     res["self"] = "name"
        #     return JsonResponse(res)
        #
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
