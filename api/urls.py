from django.contrib import admin
from django.urls import path, re_path

from api.views import login, article

urlpatterns = [
    path('login/', login.LoginView.as_view()),  # 登录
    path('register/', login.RegisterView.as_view()),  # 注册
    path('article/', article.ArticleView.as_view()),  # 凡是到article的，都认为是与添加文章有关
    re_path('article/(?P<nid>\d+)/', article.ArticleView.as_view())  # 编辑(修改)文章
]
