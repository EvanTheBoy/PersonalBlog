from django.contrib import admin
from django.urls import path

from api.views import login, article

urlpatterns = [
    path('login/', login.LoginView.as_view()),
    path('register/', login.RegisterView.as_view()),
    path('article/', article.ArticleView.as_view())  # 凡是到article的，都认为是与添加文章有关
]
