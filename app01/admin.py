from django.contrib import admin
from app01.models import Articles  # 文章表
from app01.models import Tags  # 标签
from app01.models import Cover  # 文章封面表

# Register your models here.
admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Cover)
