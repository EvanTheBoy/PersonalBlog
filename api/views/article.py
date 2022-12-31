from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery


class ArticleView(View):
    def post(self, request):
        res = {
            "msg": "文章发布成功",
            "code": 412
        }
        data: dict = request.data
        # 要求发布文章必须要填写标题和内容
        title = data.get('title')
        if not title:
            res["msg"] = "请输入文章标题"
            return JsonResponse(res)

        content = data.get('content')
        if not content:
            res['msg'] = "请输入文章内容"
            return JsonResponse(res)

        recommend = data.get('recommend')

        # 有些数据必须有，有些没有，这里先肯定有必有的数据
        # 至于那些不一定有的，管它呢，有就添加，没有拉倒
        extra = {
            "title": title,
            "content": content,
            "recommend": recommend
        }

        content = data.get('content')
        # 接下来是两个markdown的处理函数
        # 经过处理后可以得到纯文本
        # 若没有简介，获取文章内容的前30个字符
        abstract = data.get('abstract')
        if not abstract:
            abstract = PyQuery(markdown(content)).text()[:30]
        extra['abstract'] = abstract

        category = data.get('category_id')
        if category:
            extra['category'] = category

        cover_id = data.get('cover_id')
        if cover_id:
            extra['cover_id'] = cover_id
        else:
            extra['cover_id'] = 1

        pwd = data.get("pwd")
        if pwd:
            extra['pwd'] = pwd

        return JsonResponse(extra)
