import json

from django.utils.deprecation import MiddlewareMixin


# 解析post请求的数据, 反序列化
class Md1(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            request.data = data

    # 响应中间件
    def process_response(self, request, response):
        return response
