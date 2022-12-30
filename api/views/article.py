from django.views import View
from django.http import JsonResponse


class ArticleView(View):
    def post(self, request):
        return JsonResponse({})
