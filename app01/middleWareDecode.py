import json

from django.utils.deprecation import MiddlewareMixin


# 解析post请求的数据, 反序列化
# 我不想在前端处理数据，那就直接交给后端
# 目的就是每一次发送请求时都把数据进行解析，即解析json格式的数据，然后把解析完毕的数据
# 绑定到request中去，方便在后端处理（因为就可以直接获取了）
# 先经过中间件，然后去后端
class Md1(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        # 并且判断它是json的就去解析，而如果是urlencoding就不解析
        # 只有当请求方式是post的时候才做处理
        if request.method != 'GET' and request.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(request.body)
            request.data = data

    # 响应中间件
    def process_response(self, request, response):
        return response
