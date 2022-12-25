from django import forms
from django.contrib import auth
from app01.models import UserInfo
from django.views import View
from django.http import JsonResponse


# 数据库中很多具有多对多关系的表均由auth自动创建，auth是Django提供的权限管理系统
# 它可以和admin模块一起使用创建小型项目

# 在这里存放与登录相关的所有ajax请求，原先写的那个只返回页面
# 新写了页面，那么就要在settings里面注册这个api，然后对应的前端代码的请求地址也都需要修改
# 登录注册的父类——自己定义一个
class BaseForm(forms.Form):
    # 需要进行验证的三个字段
    # 这里要先定义，在后面的cleaned_data处时才能拿到
    name = forms.CharField(error_messages={"required": "请输入用户名"})
    pwd = forms.CharField(error_messages={"required": "请输入密码"})
    code = forms.CharField(error_messages={"required": "请输入验证码"})

    # 重写init方法,为了拿request,session里面保存的code.
    # 否则光有form表单，拿不到session中的code
    # 从form表单这里拿到的是用户输入的，而session中的是系统给用户生成的
    def __init__(self, *args, **kwargs):
        # 拿到请求对象, 并将其赋给self的request
        # 之所以这么干，是因为我希望在clean_code中拿到request
        self.request = kwargs.pop('request', None)

        # 让这个方法正常执行
        super().__init__(*args, **kwargs)

    # 定义局部钩子，验证验证码是否正确
    def clean_code(self):
        code: str = self.cleaned_data.get('code')
        # cleaned_data就是钩子的self自带的成员变量，通过这个我们可以拿到想要的数据
        valid_code: str = self.request.session.get('valid_code')
        if code.upper() != valid_code.upper():
            self.add_error("code", "验证码错误!")
        return self.cleaned_data


# 登录的字段验证
class LoginForm(BaseForm):
    # 定义全局钩子
    def clean(self):
        # 全局钩子的命名规则就是cleaned_'自己命的名'，这样的方式命名
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        # 这个方法就是用来验证登录信息是否正确的，当然是从数据库中取数据
        user = auth.authenticate(username=name, password=pwd)
        if not user:
            # 为字段添加错误信息
            self.add_error("pwd", "用户名或密码错误!")
        # cleaned_data本质上是一个字典。能走到这一步说明拿到了正确的user对象
        # 因此直接给它添加一个user的键值对
        self.cleaned_data['user'] = user
        return self.cleaned_data

    # 验证码的验证应该属于另外的方法，因此不应该在全局钩子中编写
    # 这部分已进行优化，添加至父类中


# 注册的字段验证
class RegisterForm(BaseForm):
    # 这里还需要单独验证一个再次输入的密码
    re_pwd = forms.CharField(error_messages={"required": "请再次输入密码"})

    # 定义全局钩子，验证两次的密码是否一致
    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致!')
        return self.cleaned_data

    # 定义局部钩子，验证用户名是否已经被使用
    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error("name", "该用户已注册!")
        return self.cleaned_data


# 登录失败的可复用代码
def clean_form(form):
    # 将错误信息存在一个字典中
    err_dict: dict = form.errors
    # 拿到所有错误字段的名字，比如name, pwd这些。通过取得字典的key值可以拿到它们
    err_valid = list(err_dict.keys())[0]
    # 拿到第一个字段的错误信息,比如“请输入用户名”这样的信息
    # 这里的第一个，指的是有错误的第一个
    err_msg = err_dict[err_valid][0]
    return err_valid, err_msg


# 用户成功登录
class LoginView(View):
    def post(self, request):
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
        # 在这里实现登录功能
        user = form.cleaned_data.get('user')
        # 登录操作
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)


# 成功注册
class RegisterView(View):
    def post(self, request):
        res = {
            'code': 1,  # 0表示登录成功
            'msg': "注册成功!",  # 提示信息
            'self': None  # 提示错误的地方
        }
        # 以下，可直接使用request.data，因为在中间件中request.data已经被赋值了
        form = RegisterForm(request.data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 注册成功
        # 先获取用户名和密码
        name = request.data.get('name')
        pwd = request.data.get('pwd')
        # 这里使用的仍然是auth模块
        user = UserInfo.objects.create_user(username=name, password=pwd)

        # 注册之后直接登录
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)
