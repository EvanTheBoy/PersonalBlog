from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from app01.utils.generateCode import generate_random_code
from django import forms
from django.contrib import auth

# Create your views here.

# 登录的字段验证
class LoginForm(forms.Form):
    name = forms.CharField(error_messages={"required": "请输入用户名"})
    pwd = forms.CharField(error_messages={"required": "请输入密码"})
    code = forms.CharField(error_messages={"required": "请输入验证码"})

    # 重写init方法,为了拿request,session里面保存的code.
    def __init__(self, *args, **kwargs):
        # 拿到请求对象, 并将其赋给这个类的request
        self.request = kwargs.pop('request', None)

        # 让这个方法正常执行
        super().__init__(*args, **kwargs)

    # 定义全局钩子
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        # 为字段添加错误信息
        user = auth.authenticate(username=name, password=pwd)
        if not user:
            self.add_error("pwd", "用户名或密码错误!")
        return self.cleaned_data

    # 验证码的验证应该属于另外的方法，因此不应该在全局钩子中编写
    def clean_code(self):
        code: str = self.cleaned_data.get('code')
        valid_code: str = self.request.session.get('valid_code')
        if code.upper() != valid_code.upper():
            self.add_error("code", "验证码错误!")
        return self.cleaned_data


def get_index(request):
    return render(request, "index.html")


def news(request):
    return render(request, "news.html")


# 登录失败的可复用代码
def clean_form(form):
    # 将错误信息存在一个字典中
    err_dict: dict = form.errors
    # 拿到所有错误字段的名字，比如name, pwd这些。通过取得字典的key值可以拿到它们
    err_valid = list(err_dict.keys())[0]
    # 拿到第一个字段的错误信息,比如“请输入用户名”这样的信息
    err_msg = err_dict[err_valid][0]
    return err_valid, err_msg


def login(request):
    if request.method == 'POST':
        res = {
            'code': 1,  # 0表示登录成功
            'msg': "登录成功!",  # 提示信息
            'self': None  # 提示错误的地方
        }
        form = LoginForm(request.data, request=request)
        if not form.is_valid():
            # 验证不通过
            # 配置res的信息
            res['self'], res['msg'] = clean_form(form)
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
