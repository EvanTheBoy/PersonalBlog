import random

from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from app01.models import Tags, Articles, Cover
from django import forms
from api.views.login import clean_form


# form表单都是把所有错误收集完毕然后一起返回
class AddArticleForm(forms.Form):
    # 以下添加了error_messages，那么在调用form.is_valid()方法时就只会验证这两个字段
    title = forms.CharField(error_messages={'required': "请输入文章标题"})
    content = forms.CharField(error_messages={'required': "请输入文章内容"})
    abstract = forms.CharField(required=False)  # required=False表示不进行为空验证，就是说它可以为空
    cover_id = forms.IntegerField(required=False)

    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)

    # 全局钩子，校验文章分类和密码
    def clean(self):
        category = self.cleaned_data.get('category')
        if not category:
            # 没有的话就不要了
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data.get('pwd')
        if not pwd:
            # 没有的话就不要了
            self.cleaned_data.pop('pwd')

    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data.get('abstract')
        if abstract:
            return abstract
        # 能走到这一步说明abstract不存在
        # 那就只能截取文章内容
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:30]
            return abstract

    # 封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data.get('cover_id')
        if cover_id:
            return cover_id
        # 调用库函数all()进行查询，返回的结果是个字典
        cover_set = Cover.objects.all().values()
        cover_id = random.choice(cover_set)['nid']
        return cover_id


class ArticleView(View):
    def post(self, request):
        res = {
            "msg": "文章发布成功",
            "code": 412,
            "data": None
        }
        data: dict = request.data
        # 直接添加一个状态的键值对
        data['status'] = 1
        form = AddArticleForm(data)
        # 校验不通过
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过，直接返回
        # 直接在form.cleaned_data中添加，否则要是在data中添加的话，前面
        # 需要先验证，太麻烦了
        form.cleaned_data['author'] = 'Evan'
        form.cleaned_data['source'] = "Evan的个人博客"
        article_pbj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        for tag in tags:
            if tag.isdigit():
                article_pbj.tag.add(tag)
            else:
                # 不是数字，那就先创建词条再添加
                tag_obj = Tags.objects.create(title=tag)
                article_pbj.tag.add(tag_obj)

        res['code'] = 0
        res['data'] = article_pbj.nid
        # res是要返回给前端的信息，而data里面是文章本身的信息
        # 不要二者搞混了
        return JsonResponse(res)

    def put(self, request, nid):
        res = {
            "msg": "文章编辑成功",
            "code": 412,
            "data": None
        }
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误'
            return JsonResponse(res)
        # 文章存在，才执行如下的代码
        data: dict = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        # 校验不通过
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过，直接返回
        form.cleaned_data['author'] = 'Evan'
        form.cleaned_data['source'] = "Evan的个人博客"
        # 用下面这个方法更新数据
        article_query.update(**form.cleaned_data)

        # 标签的话，直接全部清空，现在传了什么来就直接来什么
        tags = data.get('tags')
        article_query.first().tag.clear()
        # 这里获取的tags和从文章set中获取的tags二者不是同一个
        for tag in tags:
            if tag.isdigit():
                article_query.first().tag.add(tag)
            else:
                # 不是数字，那就先创建词条再添加
                tag_obj = Tags.objects.create(title=tag)
                article_query.first().tag.add(tag_obj)

        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)
