from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


# Create your views here.
def get_index(request):
    return render(request, "index.html")


def news(request):
    return render(request, "news.html")


def login(request):
    if request.method == 'POST':
        data = request.data
        return JsonResponse(data)
    return render(request, "login.html")


def get_random_code(request):
    fp = open(r'F:\PersonalBlogProject\app01\utils\new_img.png', 'rb')
    data = fp.read()
    fp.close()
    return HttpResponse(data)


def register(request):
    return render(request, "register.html")
