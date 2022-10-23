from django.shortcuts import render


# Create your views here.
def get_index(request):
    # 进行图片渲染
    img_list = [
        "/static/myFile/image/header/slideshow1.jpg",
        "/static/myFile/image/header/slideshow2.jpg",
        "/static/myFile/image/header/slideshow3.jpg",
        "/static/myFile/image/header/slideshow4.jpg"
    ]
    return render(request, "index.html", {"img_list": img_list})
