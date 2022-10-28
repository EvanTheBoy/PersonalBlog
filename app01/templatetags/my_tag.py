from django import template

register = template.Library()


# 这里是自定义过滤器
@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name):
    print(menu_name)
    img_list = [
        "/static/myFile/image/header/slideshow1.png",
        "/static/myFile/image/header/slideshow2.jpg",
        "/static/myFile/image/header/slideshow3.jpg",
        "/static/myFile/image/header/slideshow4.jpg",
    ]
    return {"img_list": img_list}
