from django import template

register = template.Library()


# 这里是自定义过滤器
# 这里的nid参数要给一个默认值None, 因为index那样的页面不需要nid, 而像article这样的文章是需要的
# 之所以这么改，最终可以归结为在block继承那里多加了一个参数，因为对于article而言我们需要知道是哪一篇文章
@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, nid=None):
    print(menu_name)
    img_list = [
        "/static/myFile/image/header/slideshow1.png",
        "/static/myFile/image/header/slideshow2.jpg",
        "/static/myFile/image/header/slideshow3.jpg",
        "/static/myFile/image/header/slideshow4.jpg",
    ]
    # 根据传进来的“名称”来做不同的事情，即在数据库中找到不同的数据返回到页面上
    return {"img_list": img_list}
