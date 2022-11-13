import json

from django.utils.deprecation import MiddlewareMixin


# 解析post请求的数据
class Md1(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST':
            data = json.loads(request.body, encoding='utf-8')
            request.data = data

    def process_response(self, request, response):
        return response
