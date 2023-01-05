"""PersonalBlogProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve

from app01 import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.get_index),
    path('news/', views.news),
    path('login/', views.login),
    path('register/', views.register),
    path('login/random_code/', views.get_random_code),
    path('logout/', views.logout),
    path('backend/', views.backend),  # 后台个人中心
    path('backend/add_article/', views.add_article),  # 添加文章
    path('backend/edit_avatar/', views.edit_avatar),  # 修改头像
    path('backend/reset_password/', views.reset_password),  # 重置密码
    re_path(r'^backend/edit_article/(?P<nid>\d+)/', views.edit_article),  # 编辑文章
    re_path(r'^article/(?P<nid>\d+)/', views.article),
    re_path(r'^api/', include('api.urls')),  # 路由分发，将所有以api开头的请求分发到api的urls.py中
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})  # 用户上传文件的路由配置
]
