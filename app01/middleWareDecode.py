import json

from django.utils.deprecation import MiddlewareMixin


# 解析post请求的数据, 反序列化
class Md1(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        #  并且判断它是json的就去解析，而如果是urlencoding就不解析
        if request.method == 'POST' and request.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(request.body)
            request.data = data

    # 响应中间件
    def process_response(self, request, response):
        return response
